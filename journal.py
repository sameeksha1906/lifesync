import os
from datetime import datetime
from getpass import getpass

# Path to store journal entry
JOURNAL_DIR = "my_journal"

# journal directory exists
os.makedirs(JOURNAL_DIR, exist_ok=True)

def get_today_filename():
    return os.path.join(JOURNAL_DIR, datetime.now().strftime("%Y-%m-%d") + ".txt")

def write_entry():
    print("\nStart writing your journal entry")
    entry = input("Your entry:\n")
    with open(get_today_filename(), "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    print(" Journal entry saved privately.\n")

def read_entries():
    print("\n Journal Entries ")
    files = sorted(os.listdir(JOURNAL_DIR))
    for filename in files:
        with open(os.path.join(JOURNAL_DIR, filename), "r", encoding="utf-8") as f:
            print(f"\n📅 {filename.replace('.txt','')}")
            print(f.read())

def main():
    print("Welcome to Your Private Journal ")
    while True:
        print("\nOptions:\n1. Write Entry\n2. View Entries\n3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            write_entry()
        elif choice == "2":
            read_entries()
        elif choice == "3":
            print("Bye!! Take Care.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
    
