import datetime
import calendar
from collections import defaultdict

class RoutineItem:
    """
    Represents a single routine item.

    Attributes:
        task (str): The description of the task.
        completed (bool): A flag indicating whether the task is completed.
        time (str, optional): The time of the task (e.g., "9:00 AM").
    """
    def __init__(self, task, completed=False, time=None):
        """
        Initializes a RoutineItem object.

        Args:
            task (str): The description of the task.
            completed (bool, optional): Defaults to False.
            time (str, optional): Defaults to None.
        """
        if not isinstance(task, str):
            raise TypeError("Task must be a string.")
        if not isinstance(completed, bool):
            raise TypeError("Completed must be a boolean.")
        if time is not None and not isinstance(time, str):
            raise TypeError("Time must be a string.")
        self.task = task
        self.completed = completed
        self.time = time

    def __str__(self):
        """
        Returns a string representation of the RoutineItem.
        """
        return f"{self.task} ({'Completed' if self.completed else 'Not Completed'})"

    def __repr__(self):
        """
        Official string representation for developers (useful for debugging).
        """
        return f"RoutineItem(task='{self.task}', completed={self.completed}, time='{self.time}')"


class DailyRoutine:
    """
    Represents a daily routine.

    Attributes:
        date (datetime.date): The date of the routine.
        items (list[RoutineItem]): A list of RoutineItem objects.
    """
    def __init__(self, date):
        """
        Initializes a DailyRoutine object.

        Args:
            date (datetime.date): The date of the routine.
        """
        if not isinstance(date, datetime.date):
            raise TypeError("Date must be a datetime.date object.")
        self.date = date
        self.items = []

    def add_item(self, item):
        """
        Adds a RoutineItem to the daily routine.

        Args:
            item (RoutineItem): The RoutineItem to add.
        """
        if not isinstance(item, RoutineItem):
            raise TypeError("Item must be a RoutineItem object.")
        self.items.append(item)

    def get_completion_percentage(self):
        """
        Calculates the completion percentage of the daily routine.

        Returns:
            float: The completion percentage (0-100).
        """
        if not self.items:
            return 100.0  # Return 100% for an empty routine
        completed_items = sum(item.completed for item in self.items)
        return (completed_items / len(self.items)) * 100

    def __str__(self):
        """
        Returns a string representation of the DailyRoutine.
        """
        return f"Daily Routine for {self.date}: {len(self.items)} items, {self.get_completion_percentage():.2f}% completed"

    def __repr__(self):
        """
        Official string representation.
        """
        return f"DailyRoutine(date={self.date}, items={self.items})"

    def to_dict(self):
        """
        Convert the DailyRoutine object to a dictionary.  Useful for JSON serialization.
        """
        return {
            "date": self.date.isoformat(),
            "items": [{"task": item.task, "completed": item.completed, "time": item.time} for item in self.items]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a DailyRoutine object from a dictionary. Useful for JSON deserialization
        """
        date_obj = datetime.date.fromisoformat(data['date'])
        routine = cls(date_obj)
        for item_data in data['items']:
            routine.add_item(RoutineItem(task=item_data['task'], completed=item_data['completed'], time=item_data.get('time')))
        return routine

class MonthlyReport:
    """
    Generates a monthly report of daily routines.

    Attributes:
        year (int): The year of the report.
        month (int): The month of the report.
        routines (dict[datetime.date, DailyRoutine]): A dictionary of daily routines,
            where the key is the date and the value is the DailyRoutine object.
    """
    def __init__(self, year, month, routines):
        """
        Initializes a MonthlyReport object.

        Args:
            year (int): The year of the report.
            month (int): The month of the report.
            routines (dict[datetime.date, DailyRoutine]):
        """
        if not isinstance(year, int):
            raise TypeError("Year must be an integer.")
        if not isinstance(month, int):
            raise TypeError("Month must be an integer.")
        if not isinstance(routines, dict) or not all(isinstance(k, datetime.date) and isinstance(v, DailyRoutine) for k, v in routines.items()):
            raise TypeError("Routines must be a dictionary of date: DailyRoutine.")
        self.year = year
        self.month = month
        self.routines = routines
        self.days_in_month = calendar.monthrange(year, month)[1] # Number of days in the month

    def get_average_completion(self):
        """
        Calculates the average completion percentage for the month.

        Returns:
            float: The average completion percentage.
        """
        total_completion = 0
        valid_days = 0 # Count days with routines
        for day in range(1, self.days_in_month + 1):
            date = datetime.date(self.year, self.month, day)
            if date in self.routines:
                total_completion += self.routines[date].get_completion_percentage()
                valid_days += 1
        return total_completion / valid_days if valid_days > 0 else 100.0

    def get_completed_days(self):
        """
        Gets the number of days with 100% completion.

        Returns:
            int: The number of fully completed days.
        """
        completed_days = 0
        for day in range(1, self.days_in_month + 1):
            date = datetime.date(self.year, self.month, day)
            if date not in self.routines:
                continue
            if self.routines[date].get_completion_percentage() == 100:
                completed_days += 1
        return completed_days

    def get_report(self):
        """
        Generates a detailed monthly report.

        Returns:
            str: The formatted monthly report.
        """
        report = f"Monthly Report for {calendar.month_name[self.month]} {self.year}\n"
        report += f"--------------------------------------------------------\n"
        report += f"Average Completion: {self.get_average_completion():.2f}%\n"
        report += f"Days with 100% Completion: {self.get_completed_days()} / {self.days_in_month}\n"
        report += "\nDaily Routine Details:\n"
        for day in range(1, self.days_in_month + 1):
            date = datetime.date(self.year, self.month, day)
            if date in self.routines:
                report += f"\n  {date}:\n"
                for item in self.routines[date].items:
                    report += f"    - {item}\n"
            else:
                report += f"\n  {date}: No routine recorded\n"

        report += "\nAnalysis and Recommendations:\n"
        report += self.get_analysis_and_recommendations()
        return report

    def get_analysis_and_recommendations(self):
        """
        Analyzes the monthly routine data and provides recommendations.

        This is where the core logic for health-related analysis and recommendations
        would go.  This is a placeholder.
        """
        analysis = ""
        recommendations = ""
        average_completion = self.get_average_completion()
        completed_days = self.get_completed_days()

        if average_completion < 70:
            analysis += "Low average completion rate suggests inconsistency in following the routine.\n"
            recommendations += "Try to schedule tasks at specific times and set reminders.  Break down larger tasks into smaller, more manageable steps.\n"
        elif average_completion < 90:
            analysis += "Good average completion rate, but there's room for improvement.\n"
            recommendations += "Identify the reasons for incomplete tasks and find strategies to overcome them.  Consider adding some flexibility to your schedule.\n"
        else:
            analysis += "Excellent average completion rate!  You are consistently following your routine.\n"
            recommendations += "Keep up the good work!  Consider adding new healthy habits to your routine.\n"

        if completed_days < 15:
            analysis += "Low number of days with 100% completion indicates that you often miss completing all tasks.\n"
            recommendations += "Evaluate if your daily routine is realistic and sustainable.  Prioritize essential tasks and be flexible with less important ones.\n"
        elif completed_days < 25:
            analysis += "A fair number of days with 100% completion.\n"
            recommendations += "Try to identify what helps you complete all tasks and do more of that.  Ensure you have enough time for each task.\n"
        else:
            analysis += "Great job on completing all tasks on most days!\n"
            recommendations += "Maintain your discipline and consistency.  You may want to reflect on how your routine makes you feel.\n"

        # Placeholder for specific health-related analysis (e.g., sleep, exercise)
        #  Needs more data about the routine items.
        analysis += "\n[Placeholder for specific health-related analysis]\n"
        recommendations += "[Placeholder for specific health recommendations based on routine data]\n"

        return analysis + "\n" + recommendations
    
    def display_report(self):
        """Prints the monthly report to the console."""
        print(self.get_report())

def main():
    """
    Main function to run the daily routine tracker and generate a monthly report.
    """
    routines = {}
    year = 2024
    month = 12

    # Pre-populate some data for demonstration and testing.
    #  Using datetime.date objects directly.
    routine1_date = datetime.date(year, month, 1)
    routine1 = DailyRoutine(routine1_date)
    routine1.add_item(RoutineItem("Wake up", True, "7:00 AM"))
    routine1.add_item(RoutineItem("Exercise", False, "8:00 AM"))
    routine1.add_item(RoutineItem("Breakfast", True, "9:00 AM"))
    routines[routine1_date] = routine1

    routine2_date = datetime.date(year, month, 5)
    routine2 = DailyRoutine(routine2_date)
    routine2.add_item(RoutineItem("Work", True, "9:00 AM"))
    routine2.add_item(RoutineItem("Lunch", True, "1:00 PM"))
    routine2.add_item(RoutineItem("Work", True, "2:00 PM"))
    routine2.add_item(RoutineItem("Dinner", False, "7:00 PM"))
    routines[routine2_date] = routine2
    
    routine3_date = datetime.date(year, month, 6)
    routine3 = DailyRoutine(routine3_date)
    routine3.add_item(RoutineItem("Sleep", False, "10:00 PM"))
    routines[routine3_date] = routine3
    
    routine4_date = datetime.date(year, month, 7)
    routine4 = DailyRoutine(routine4_date)
    routines[routine4_date] = routine4 #empty routine
    
    routine5_date = datetime.date(year, month, 31)
    routine5 = DailyRoutine(routine5_date)
    routine5.add_item(RoutineItem("Wake up", True, "7:00 AM"))
    routine5.add_item(RoutineItem("Go for a run", True, "8:00 AM"))
    routine5.add_item(RoutineItem("Have breakfast", True, "9:00 AM"))
    routine5.add_item(RoutineItem("Work", True, "10:00 AM"))
    routine5.add_item(RoutineItem("Lunch", True, "1:00 PM"))
    routine5.add_item(RoutineItem("Work", True, "2:00 PM"))
    routine5.add_item(RoutineItem("Dinner", True, "7:00 PM"))
    routine5.add_item(RoutineItem("Relax", True, "8:00 PM"))
    routine5.add_item(RoutineItem("Sleep", True, "10:00 PM"))
    routines[routine5_date] = routine5

    # Create and display the monthly report.
    report = MonthlyReport(year, month, routines)
    report.display_report()

if __name__ == "__main__":
    main()
