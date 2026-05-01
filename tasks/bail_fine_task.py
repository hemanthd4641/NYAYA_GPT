# tasks/bail_fine_task.py

from crewai import Task
from agents.legal_procedural_agent import legal_procedural_agent
from tasks.legal_research_task import legal_research_task

bail_fine_task = Task(
    agent=legal_procedural_agent,
    description=(
        "Review the legal sections identified by the Research Agent.\n\n"
        "1. Extract the punishment and fine details for each section.\n"
        "2. Determine if the overall case is Bailable or Non-Bailable (if any section is Non-Bailable, the case is usually treated as such).\n"
        "3. Provide a summary of the 'Procedural Outlook' including the maximum potential jail time and the total fine range."
    ),
    expected_output=(
        "A clear breakdown of:\n"
        "- Bail Status (Bailable/Non-Bailable)\n"
        "- Punishment Range (e.g., 2-5 years)\n"
        "- Fine Estimates\n"
        "- Cognizability Status"
    ),
    context=[legal_research_task]
)
