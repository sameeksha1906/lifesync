# journal_logic.py
import os
from datetime import datetime

# Path to store journal entry
JOURNAL_DIR = "my_journal"

# Ensure journal directory exists
os.makedirs(JOURNAL_DIR, exist_ok=True)

def get_today_filename():
    return os.path.join(JOURNAL_DIR, datetime.now().strftime("%Y-%m-%d") + ".txt")

def write_journal_entry(entry_text):
    """Writes a new journal entry."""
    if not entry_text.strip():
        return False, "Entry cannot be empty."
    with open(get_today_filename(), "a", encoding="utf-8") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write(entry_text + "\n\n")
    return True, "Journal entry saved privately."

def read_journal_entries():
    """Reads all journal entries, sorted by filename (date)."""
    entries_data = []
    if not os.path.exists(JOURNAL_DIR):
        return entries_data
        
    files = sorted(os.listdir(JOURNAL_DIR), reverse=True) # Show newest first
    for filename in files:
        if filename.endswith(".txt"):
            date_str = filename.replace('.txt','')
            try:
                # Validate date format if needed, though strftime should be consistent
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                continue # Skip files not matching the date format

            with open(os.path.join(JOURNAL_DIR, filename), "r", encoding="utf-8") as f:
                entries_data.append({"date": date_str, "content": f.read()})
    return entries_data
