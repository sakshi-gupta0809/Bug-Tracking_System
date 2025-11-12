# Functions to load and save data will go here
import json
import os

BUGS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'bugs.json')

def load_bugs():
    if not os.path.exists(BUGS_FILE):
        return []
    with open(BUGS_FILE, 'r') as f:
        return json.load(f)

def save_bugs(bugs):
    with open(BUGS_FILE, 'w') as f:
        json.dump(bugs, f, indent=2)
