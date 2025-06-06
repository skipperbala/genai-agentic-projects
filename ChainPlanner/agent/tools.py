from datetime import datetime


def get_calendar_events(date: str) -> str:
    events = {
        "2025-05-15": [
            {"time": "09:00 - 10:00", "event": "Team standup"},
            {"time": "14:00 - 15:30", "event": "Client meeting"},
        ],
        "default": [
            {"time": "10:00 - 11:00", "event": "Deep work session"},
            {"time": "16:00 - 17:00", "event": "Gym"}
        ]
    }
    items = events.get(date, events["default"])
    return "\n".join([f"{item['time']}: {item['event']}" for item in items])

def get_todo_list(date: str) -> str:
    todos = {
        "2025-05-15": [
            "Finish quarterly report",
            "Reply to investor email",
            "Read 10 pages of Atomic Habits"
        ],
        "default": [
            "Plan weekly goals",
            "Write blog draft",
            "Call parents"
        ]
    }
    items = todos.get(date, todos["default"])
    return "\n".join([f"- {item}" for item in items])
