import os
import json
import datetime
import random
DATA_DIR = "lifesync_data"

class LifeSyncApp:
    def __init__(self, username):
        self.username = username.lower().strip()
        self.user_dir = os.path.join(DATA_DIR, self.username)
        os.makedirs(self.user_dir, exist_ok=True)

    def write_journal(self):
        date = datetime.date.today().isoformat()
        path = os.path.join(self.user_dir, f"journal_{date}.txt")
        print(f"\nWrite your journal for {date}")
        entry = input("Your thoughts:\n> ")
        with open(path, "w", encoding="utf-8") as f:
            f.write(entry)
        print("Journal saved privately.")

    def track_routine(self):
        print("\n Daily Routine Tracking")
        routine = {
            "date": str(datetime.date.today()),
            "steps_walked": input("Steps walked today: "),
            "sleep_time": input("When did you go to sleep? (e.g., 10:30 PM): "),
            "wake_time": input("When did you wake up? (e.g., 6:30 AM): "),
            "meals": input("What did you eat today?: "),
            "diet_plan_followed": input("Did you follow your diet plan? (yes/no): ")
        }
        path = os.path.join(self.user_dir, "routine.json")
        routines = {}
        if os.path.exists(path):
            routines = json.load(open(path))
        routines[routine["date"]] = routine
        with open(path, "w") as f:
            json.dump(routines, f, indent=2)
        print(" Routine saved.")

    def health_and_therapy(self):
        print("\n🩺 Health & Therapy")
        history_path = os.path.join(self.user_dir, "health.json")
        if os.path.exists(history_path):
            history = json.load(open(history_path))
        else:
            history = {}

        print("Describe your past health issues (e.g., diabetes, anxiety):")
        history["past_issues"] = input("> ")
        print("Any new symptoms or concerns today?")
        history["current_symptoms"] = input("> ")

        # Simple logic for risk detection (can be replaced by ML later)
        if "anxiety" in history["past_issues"].lower() or "stress" in history["current_symptoms"].lower():
            print(" You may be prone to stress-related conditions. Consider relaxation therapy.")
        if "diabetes" in history["past_issues"].lower() or "sugar" in history["current_symptoms"].lower():
            print(" Monitor blood sugar and follow a low-carb diet.")

        with open(history_path, "w") as f:
            json.dump(history, f, indent=2)

        print("Would you like to schedule an online therapy session? (not implemented)")
        input("Press Enter to continue...")

    def ai_chatbot(self):
        print("\n🤖 AI Chatbot (Prototype)")
        print("Talk to me. Type 'bye' to exit.\n")
        general_responses = [
        "I'm here for you. Want to talk more about it?",
        "That sounds tough. Would you like to share more?",
        "I'm listening. Go on...",
        "You're not alone. Tell me more.",
        "Let it out — what’s on your mind?"
    ]

        mood_responses = {
        "sad": "I'm sorry you're feeling that way. Sometimes journaling helps you reflect and feel lighter.",
        "anxious": "That’s okay. Take a deep breath. Would you like a grounding tip?",
        "stress": "Stress can be overwhelming. Try closing your eyes and taking 3 deep breaths.",
        "happy": "That’s great to hear! What made you happy today?",
        "motivate": "Remember, progress is progress — even small steps count!"
    }

        while True:
            msg = input("You: ").strip().lower()
            if msg == "bye":
                print("Chatbot: I'm always here if you need to talk. 👋")
                break

        found = False
        for keyword in mood_responses:
            if keyword in msg:
                print("Chatbot:", mood_responses[keyword])
                found = True
                break

            if not found:
                print("Chatbot:", random.choice(general_responses))
    def menu(self):
        while True:
            print(f"\n LifeSync Menu for {self.username}")
            print("1. Write in Journal")
            print("2. Track Daily Routine")
            print("3. Health & Therapy")
            print("4. Talk to AI Chatbot")
            print("5. Exit")
            choice = input("Select an option: ")

        if choice == "1":
            self.write_journal()
        elif choice == "2":                self.track_routine()
        elif choice == "3":
            self.health_and_therapy()
        elif choice == "4":
            self.ai_chatbot()
        elif choice == "5":
            print("Goodbye! Stay well.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    print("Welcome to LifeSync")
    user = input("Enter your username: ")
    app = LifeSyncApp(user)
    app.menu()

