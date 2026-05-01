# tasks/timeline_task.py

from crewai import Task
from agents.timeline_agent import timeline_agent

timeline_task = Task(
    agent=timeline_agent,
    description=(
        "Analyze the following legal description:\n\n"
        "{user_input}\n\n"
        "Extract all mentioned dates, times, and significant events. "
        "Organize them in chronological order. If specific dates are missing, "
        "use relative terms (e.g., 'Shortly after', 'The next day')."
    ),
    expected_output=(
        "A visually appealing markdown timeline of the case. "
        "Use emojis like 📅 or 🕒 and vertical bars (|) to represent the flow of time. "
        "Example format:\n"
        "📅 **Date/Time** | 📝 **Event Description**\n"
        "---|---\n"
        "📅 Monday, 10 PM | User parked their vehicle.\n"
        "🕒 Tuesday, 2 AM | Suspicious noise heard."
    ),
)
