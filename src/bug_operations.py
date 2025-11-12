# Bug operations functions (add, update, delete, view) will go here
from .data_handler import load_bugs, save_bugs

def add_bug(title, description, priority):
    bugs = load_bugs()
    new_bug = {
        "id": bugs[-1]['id'] + 1 if bugs else 1,
        "title": title,
        "description": description,
        "status": "open",
        "priority": priority
    }
    bugs.append(new_bug)
    save_bugs(bugs)
    return new_bug

def list_bugs():
    return load_bugs()

def update_bug_status(bug_id, new_status):
    bugs = load_bugs()
    for bug in bugs:
        if bug['id'] == bug_id:
            bug['status'] = new_status
            save_bugs(bugs)
            return True
    return False

def delete_bug(bug_id):
    bugs = load_bugs()
    updated_bugs = [bug for bug in bugs if bug['id'] != bug_id]
    if len(bugs) == len(updated_bugs):
        return False
    save_bugs(updated_bugs)
    return True
