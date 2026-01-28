import os
import json

def get_saved_lists_path():
    """Return the absolute path to the saved_lists.json file."""
    return os.path.join(os.path.dirname(__file__), "saved_lists.json")

def load_lists():
    """Load lists from the JSON file."""
    path = get_saved_lists_path()
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading lists: {e}")
    return {}

def save_lists(lists_dict):
    """Save the lists dictionary to the JSON file."""
    path = get_saved_lists_path()
    try:
        with open(path, "w") as f:
            json.dump(lists_dict, f, indent=4)
    except Exception as e:
        print(f"Error saving lists: {e}")
