# tasks/legal_research_task.py

from crewai import Task
from agents.legal_research_agent import legal_research_agent

legal_research_task = Task(
    agent=legal_research_agent,
    description=(
        "Research and identify all applicable legal sections across different Indian Acts "
        "for the following legal situation:\n\n"
        "{user_input}\n\n"
        "Analyze the case carefully. If it involves digital data, check the IT Act. "
        "If it involves procedure or bail, check CrPC. If it involves evidence, check IEA. "
        "Always check the IPC for core offenses."
    ),
    expected_output=(
        "A structured list of relevant sections from various Acts. "
        "For each section, provide the Act name, Section number, Title, and a brief explanation of how it applies."
    ),
)
