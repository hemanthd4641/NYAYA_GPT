# tasks/matchmaker_task.py

from crewai import Task
from agents.matchmaker_agent import matchmaker_agent
from tasks.case_intake_task import case_intake_task

matchmaker_task = Task(
    agent=matchmaker_agent,
    description=(
        "Review the analyzed case data, including the legal domain and case type:\n\n"
        "Recommend the exact type of specialist lawyer or legal expert the user should hire. "
        "Explain briefly why this specific expertise is necessary for their situation."
    ),
    expected_output=(
        "A clear, professional recommendation. "
        "Example: 'You should consult a **Criminal Defense Lawyer** specializing in **White-Collar Crime** because your case involves complex financial allegations...'"
    ),
    context=[case_intake_task]
)
