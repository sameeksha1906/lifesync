# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from datetime import datetime, date
import calendar  # For month names

# Import logic functions/classes
from journal import write_journal_entry, read_journal_entries, JOURNAL_DIR
from dailytracker import (
    RoutineItem,
    DailyRoutine,
    MonthlyReport,
    load_routines,
    save_routines,
    get_or_create_routine,
)
from attractions import attractions_manager  # Use the global instance

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flashing messages


# --- Helper ---
def get_selected_date(request_args):
    date_str = request_args.get("date")
    if date_str:
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            flash("Invalid date format. Showing today's routine.", "warning")
            return date.today()
    return date.today()


# --- Routes ---
@app.route("/")
def index():
    # Your existing index.html for login
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    # This page is shown after "login"
    return render_template("dashboard.html")


# --- Journal Feature ---
@app.route("/journal", methods=["GET", "POST"])
def journal_page():
    if request.method == "POST":
        entry_text = request.form.get("entry_text")
        if entry_text:
            success, message = write_journal_entry(entry_text)
            if success:
                flash(message, "success")
            else:
                flash(message, "danger")
            return redirect(url_for("journal_page"))
        else:
            flash("Entry cannot be empty.", "warning")

    entries = read_journal_entries()
    return render_template(
        "journal_page.html",
        entries=entries,
        today_date=date.today().strftime("%Y-%m-%d"),
    )


# --- Daily Routine Tracker Feature ---
all_routines_data = (
    load_routines()
)  # Load once at app start, or move inside route if frequent updates from elsewhere


@app.route("/routine", methods=["GET"])
def routine_page():
    global all_routines_data
    selected_date_obj = get_selected_date(request.args)
    current_routine = get_or_create_routine(selected_date_obj, all_routines_data)

    monthly_report_data = None
    if request.args.get("view_report"):
        try:
            report_month = int(request.args.get("report_month", date.today().month))
            report_year = int(request.args.get("report_year", date.today().year))
            if 1 <= report_month <= 12:
                report_generator = MonthlyReport(
                    report_year, report_month, all_routines_data
                )
                monthly_report_data = report_generator.get_report_data()
            else:
                flash("Invalid month selected for report.", "warning")
        except ValueError:
            flash("Invalid year or month for report.", "warning")

    return render_template(
        "routine_page.html",
        routine=current_routine,
        selected_date_iso=selected_date_obj.isoformat(),
        selected_date_str=selected_date_obj.strftime("%A, %B %d, %Y"),
        monthly_report_data=monthly_report_data,
        current_month=date.today().month,
        current_year=date.today().year,
        month_names={i: calendar.month_name[i] for i in range(1, 13)},
    )


@app.route("/routine/add_item", methods=["POST"])
def add_routine_item():
    global all_routines_data
    routine_date_str = request.form.get("routine_date")
    task_name = request.form.get("task")
    task_time = request.form.get("time")  # Optional

    if not routine_date_str or not task_name:
        flash("Missing date or task name.", "danger")
        return redirect(url_for("routine_page"))

    try:
        routine_date_obj = date.fromisoformat(routine_date_str)
        routine = get_or_create_routine(routine_date_obj, all_routines_data)
        # Check for duplicate task name for the same day
        if any(item.task == task_name for item in routine.items):
            flash(f"Task '{task_name}' already exists for this day.", "warning")
        else:
            routine.add_item(
                RoutineItem(task_name, time=task_time if task_time else None)
            )
            save_routines(all_routines_data)
            flash(f"Item '{task_name}' added to routine.", "success")
    except ValueError:
        flash("Invalid date format for routine item.", "danger")

    return redirect(url_for("routine_page", date=routine_date_str))


@app.route("/routine/toggle_item", methods=["POST"])
def toggle_routine_item():
    global all_routines_data
    routine_date_str = request.form.get("routine_date")
    task_name = request.form.get("task_name")
    status_str = request.form.get("status")  # 'complete' or 'incomplete'

    if not routine_date_str or not task_name or not status_str:
        flash("Missing data to update item.", "danger")
        return redirect(
            url_for(
                "routine_page",
                date=routine_date_str if routine_date_str else date.today().isoformat(),
            )
        )

    try:
        routine_date_obj = date.fromisoformat(routine_date_str)
        routine = get_or_create_routine(routine_date_obj, all_routines_data)

        completed = True if status_str == "complete" else False

        item_found = False
        for item in routine.items:
            if item.task == task_name:
                item.completed = completed
                item_found = True
                break

        if item_found:
            save_routines(all_routines_data)
            flash(
                f"Task '{task_name}' marked as {'completed' if completed else 'not completed'}.",
                "success",
            )
        else:
            flash(f"Task '{task_name}' not found.", "warning")

    except ValueError:
        flash("Invalid date format for toggling item.", "danger")

    return redirect(url_for("routine_page", date=routine_date_str))


@app.route("/routine/delete_item", methods=["POST"])
def delete_routine_item():
    global all_routines_data
    routine_date_str = request.form.get("routine_date")
    task_name_to_delete = request.form.get("task_name")

    if not routine_date_str or not task_name_to_delete:
        flash("Missing data to delete item.", "danger")
        return redirect(
            url_for(
                "routine_page",
                date=routine_date_str if routine_date_str else date.today().isoformat(),
            )
        )

    try:
        routine_date_obj = date.fromisoformat(routine_date_str)
        if routine_date_str in all_routines_data:
            routine = all_routines_data[routine_date_str]
            initial_item_count = len(routine.items)
            routine.items = [
                item for item in routine.items if item.task != task_name_to_delete
            ]

            if len(routine.items) < initial_item_count:
                save_routines(all_routines_data)
                flash(f"Task '{task_name_to_delete}' deleted.", "success")
            else:
                flash(f"Task '{task_name_to_delete}' not found to delete.", "warning")
        else:
            flash("Routine for the specified date not found.", "warning")

    except ValueError:
        flash("Invalid date format for deleting item.", "danger")

    return redirect(url_for("routine_page", date=routine_date_str))


# --- Health and Therapy Spots Feature ---
@app.route("/health_therapy")
def health_page():
    selected_category = request.args.get("category", "")
    categories = attractions_manager.get_categories()

    if selected_category:
        att_list = attractions_manager.get_attractions_by_category(selected_category)
    else:
        att_list = attractions_manager.get_all_attractions()

    return render_template(
        "health_page.html",
        attractions_list=att_list,
        categories=categories,
        selected_category=selected_category,
    )


# --- AI Chatbot (Prototype) ---
@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot_page.html")


# No backend for chatbot in this version, handled by frontend JS prototype.
# If you want a backend:
# @app.route('/chatbot/send', methods=['POST'])
# def chatbot_send():
#     user_message = request.json.get('message')
#     # Simple echo or basic logic for prototype
#     bot_response = f"Prototype received: {user_message}"
#     if "hello" in user_message.lower():
#         bot_response = "Hello there! How can I help you (as a prototype)?"
#     return jsonify({"reply": bot_response})


if __name__ == "__main__":
    # Create the journal directory if it doesn't exist
    if not os.path.exists(JOURNAL_DIR):
        os.makedirs(JOURNAL_DIR)
    app.run(debug=True)
