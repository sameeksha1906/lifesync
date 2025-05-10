# dailytracker_logic.py
import datetime
import calendar
from collections import defaultdict
import json
import os

ROUTINES_FILE = "routines_data.json"

class RoutineItem:
    """Represents a single routine item."""
    def __init__(self, task, completed=False, time=None):
        if not isinstance(task, str):
            raise TypeError("Task must be a string.")
        if not isinstance(completed, bool):
            raise TypeError("Completed must be a boolean.")
        if time is not None and not isinstance(time, str): # Allow empty string for time
            raise TypeError("Time must be a string or None.")
        self.task = task
        self.completed = completed
        self.time = time if time else "" # Store empty string if None

    def __str__(self):
        time_str = f" (Time: {self.time})" if self.time else ""
        return f"{self.task}{time_str} - {'Completed' if self.completed else 'Not Completed'}"

    def __repr__(self):
        return f"RoutineItem(task='{self.task}', completed={self.completed}, time='{self.time}')"

    def to_dict(self):
        return {"task": self.task, "completed": self.completed, "time": self.time}

    @classmethod
    def from_dict(cls, data):
        return cls(task=data['task'], completed=data['completed'], time=data.get('time'))


class DailyRoutine:
    """Represents a daily routine."""
    def __init__(self, date):
        if not isinstance(date, datetime.date):
            # Attempt to convert if string
            if isinstance(date, str):
                try:
                    date = datetime.date.fromisoformat(date)
                except ValueError:
                    raise TypeError("Date must be a datetime.date object or valid ISO format string.")
            else:
                raise TypeError("Date must be a datetime.date object or valid ISO format string.")
        self.date = date
        self.items = []

    def add_item(self, item):
        if not isinstance(item, RoutineItem):
            raise TypeError("Item must be a RoutineItem object.")
        self.items.append(item)

    def mark_item_complete(self, task_name, completed_status=True):
        for item in self.items:
            if item.task == task_name:
                item.completed = completed_status
                return True
        return False # Item not found

    def get_completion_percentage(self):
        if not self.items:
            return 0.0 # Changed to 0.0 for no items, 100% felt misleading
        completed_items = sum(item.completed for item in self.items)
        return (completed_items / len(self.items)) * 100

    def __str__(self):
        return f"Daily Routine for {self.date}: {len(self.items)} items, {self.get_completion_percentage():.2f}% completed"

    def __repr__(self):
        return f"DailyRoutine(date={self.date}, items={self.items})"

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "items": [item.to_dict() for item in self.items]
        }

    @classmethod
    def from_dict(cls, data):
        date_obj = datetime.date.fromisoformat(data['date'])
        routine = cls(date_obj)
        for item_data in data['items']:
            routine.add_item(RoutineItem.from_dict(item_data))
        return routine


class MonthlyReport:
    """Generates a monthly report of daily routines."""
    def __init__(self, year, month, routines_dict): # routines_dict is {date_iso_str: DailyRoutine_obj}
        if not isinstance(year, int):
            raise TypeError("Year must be an integer.")
        if not isinstance(month, int):
            raise TypeError("Month must be an integer.")
        if not isinstance(routines_dict, dict):
            raise TypeError("Routines must be a dictionary.")
        self.year = year
        self.month = month
        # Filter routines for the given month and year
        self.routines_for_month = {}
        for date_str, routine_obj in routines_dict.items():
            date_obj = datetime.date.fromisoformat(date_str)
            if date_obj.year == year and date_obj.month == month:
                self.routines_for_month[date_obj] = routine_obj
        
        self.days_in_month = calendar.monthrange(year, month)[1]

    def get_average_completion(self):
        total_completion = 0
        valid_days = 0
        for day in range(1, self.days_in_month + 1):
            date = datetime.date(self.year, self.month, day)
            if date in self.routines_for_month:
                total_completion += self.routines_for_month[date].get_completion_percentage()
                valid_days += 1
        return total_completion / valid_days if valid_days > 0 else 0.0

    def get_completed_days(self):
        completed_days = 0
        for day in range(1, self.days_in_month + 1):
            date = datetime.date(self.year, self.month, day)
            if date not in self.routines_for_month:
                continue
            if self.routines_for_month[date].get_completion_percentage() == 100 and self.routines_for_month[date].items: # Ensure 100% on non-empty list
                completed_days += 1
        return completed_days

    def get_report_data(self):
        """Generates a detailed monthly report as a dictionary."""
        daily_details = []
        for day in range(1, self.days_in_month + 1):
            date = datetime.date(self.year, self.month, day)
            if date in self.routines_for_month:
                routine = self.routines_for_month[date]
                daily_details.append({
                    "date": date.isoformat(),
                    "items": [str(item) for item in routine.items],
                    "completion": f"{routine.get_completion_percentage():.2f}%"
                })
            else:
                daily_details.append({
                    "date": date.isoformat(),
                    "items": ["No routine recorded"],
                    "completion": "N/A"
                })
        
        analysis, recommendations = self.get_analysis_and_recommendations_data()

        return {
            "month_year": f"{calendar.month_name[self.month]} {self.year}",
            "average_completion": f"{self.get_average_completion():.2f}%",
            "fully_completed_days": f"{self.get_completed_days()} / {len(self.routines_for_month)} (recorded days)", # Changed to recorded days
            "total_days_in_month": self.days_in_month,
            "daily_details": daily_details,
            "analysis": analysis,
            "recommendations": recommendations
        }

    def get_analysis_and_recommendations_data(self):
        analysis_pts = []
        recommendations_pts = []
        average_completion = self.get_average_completion()
        completed_days = self.get_completed_days()

        if not self.routines_for_month: # No data for the month
            analysis_pts.append("No routine data recorded for this month.")
            recommendations_pts.append("Start tracking your daily routines to gain insights.")
            return analysis_pts, recommendations_pts

        if average_completion < 70:
            analysis_pts.append("Low average completion rate suggests inconsistency in following the routine.")
            recommendations_pts.append("Try to schedule tasks at specific times and set reminders. Break down larger tasks into smaller, more manageable steps.")
        elif average_completion < 90:
            analysis_pts.append("Good average completion rate, but there's room for improvement.")
            recommendations_pts.append("Identify the reasons for incomplete tasks and find strategies to overcome them. Consider adding some flexibility to your schedule.")
        else:
            analysis_pts.append("Excellent average completion rate! You are consistently following your routine.")
            recommendations_pts.append("Keep up the good work! Consider adding new healthy habits to your routine.")

        # Using number of days in month for completed days target
        if completed_days < self.days_in_month * 0.5: # Less than half the month fully completed
            analysis_pts.append("Low number of days with 100% completion indicates that you often miss completing all tasks.")
            recommendations_pts.append("Evaluate if your daily routine is realistic and sustainable. Prioritize essential tasks and be flexible with less important ones.")
        elif completed_days < self.days_in_month * 0.8: # Less than 80% of the month fully completed
            analysis_pts.append("A fair number of days with 100% completion.")
            recommendations_pts.append("Try to identify what helps you complete all tasks and do more of that. Ensure you have enough time for each task.")
        else:
            analysis_pts.append("Great job on completing all tasks on most days!")
            recommendations_pts.append("Maintain your discipline and consistency. You may want to reflect on how your routine makes you feel.")
        
        # Placeholder for specific health-related analysis (e.g., sleep, exercise)
        analysis_pts.append("[Placeholder for specific health-related analysis based on task names, e.g., tracking 'Exercise' or 'Sleep' tasks.]")
        recommendations_pts.append("[Placeholder for specific health recommendations based on routine data.]")

        return analysis_pts, recommendations_pts


# --- Persistence Functions ---
def load_routines():
    """Loads routines from JSON file."""
    if not os.path.exists(ROUTINES_FILE):
        return {} # Return empty dict if file doesn't exist
    try:
        with open(ROUTINES_FILE, 'r') as f:
            data = json.load(f)
        routines = {}
        for date_str, routine_data_list in data.items(): # Expecting {date_str: [item_dicts]}
            # This needs to be fixed. Should be {date_str: routine_dict}
            # For now, assuming the structure saved by save_routines is:
            # { "date_iso_string": {"date": "date_iso_string", "items": [item_dicts]} }
            if "date" in routine_data_list and "items" in routine_data_list:
                 routines[date_str] = DailyRoutine.from_dict(routine_data_list)
            else: # Try to adapt from an older format if necessary, or log an error
                print(f"Warning: Skipping malformed routine data for date {date_str}")
        return routines
    except (json.JSONDecodeError, IOError, TypeError) as e:
        print(f"Error loading routines: {e}. Starting with an empty routine set.")
        return {}


def save_routines(routines_dict): # routines_dict is {date_iso_str: DailyRoutine_obj}
    """Saves routines to JSON file."""
    serializable_routines = {date_str: routine.to_dict() for date_str, routine in routines_dict.items()}
    with open(ROUTINES_FILE, 'w') as f:
        json.dump(serializable_routines, f, indent=4)

def get_or_create_routine(date_obj, routines_dict):
    """Gets routine for a date, or creates a new one if not exists."""
    date_str = date_obj.isoformat()
    if date_str not in routines_dict:
        routines_dict[date_str] = DailyRoutine(date_obj)
    return routines_dict[date_str]

# Example usage within this file (for testing)
if __name__ == "__main__":
    # Test loading/saving
    all_routines = load_routines()

    # Get today's routine
    today = datetime.date.today()
    todays_routine = get_or_create_routine(today, all_routines)
    
    if not todays_routine.items: # Add items if new
        todays_routine.add_item(RoutineItem("Wake up", time="7:00 AM"))
        todays_routine.add_item(RoutineItem("Exercise", time="7:30 AM"))
        todays_routine.add_item(RoutineItem("Breakfast", time="8:30 AM"))

    # Mark an item
    todays_routine.mark_item_complete("Wake up", True)
    print(todays_routine)

    # Save changes
    save_routines(all_routines)

    # Generate a report for the current month
    report_generator = MonthlyReport(today.year, today.month, all_routines)
    report_data = report_generator.get_report_data()
    
    print(f"\n--- Monthly Report for {report_data['month_year']} ---")
    print(f"Average Completion: {report_data['average_completion']}")
    print(f"Fully Completed Days: {report_data['fully_completed_days']} out of {report_data['total_days_in_month']} total days")
    print("\nAnalysis:")
    for pt in report_data['analysis']: print(f"- {pt}")
    print("\nRecommendations:")
    for pt in report_data['recommendations']: print(f"- {pt}")
