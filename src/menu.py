# Menu logic will go here
# from .bug_operations import add_bug, list_bugs, update_bug_status, delete_bug
# src/menu.py
# from .bug_operations import add_bug, list_bugs, update_bug_status, delete_bug
from .bug_operations import add_bug, list_bugs, update_bug_status, delete_bug


def show_menu():
    while True:
        print("\n🐞 Bug Tracking System Menu:")
        print("1. Add Bug")
        print("2. View Bugs")
        print("3. Update Bug Status")
        print("4. Delete Bug")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            title = input("Bug Title: ")
            desc = input("Description: ")
            priority = input("Priority (low/medium/high): ")
            bug = add_bug(title, desc, priority)
            print("✅ Bug added:", bug)

        elif choice == '2':
            bugs = list_bugs()
            if not bugs:
                print("No bugs found.")
            for bug in bugs:
                print(f"[{bug['id']}] {bug['title']} - {bug['status']} - {bug['priority']}")

        elif choice == '3':
            bug_id = int(input("Bug ID: "))
            status = input("New status (open/closed): ")
            if update_bug_status(bug_id, status):
                print("✅ Status updated.")
            else:
                print("❌ Bug not found.")

        elif choice == '4':
            bug_id = int(input("Bug ID to delete: "))
            if delete_bug(bug_id):
                print("✅ Bug deleted.")
            else:
                print("❌ Bug not found.")

        elif choice == '5':
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("Invalid choice.")
