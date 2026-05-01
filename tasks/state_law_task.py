# tasks/state_law_task.py

from crewai import Task
from agents.state_law_agent import state_law_agent
from tasks.legal_research_task import legal_research_task

state_law_task = Task(
    agent=state_law_agent,
    description=(
        "The previous agent analyzed the case and identified the relevant jurisdiction (State/UT). "
        "Your task is to research if that specific state has any "
        "amendments or local variations for the identified legal sections. "
        "If the state is not explicitly identified, try to infer it from the user's description, "
        "or research if any major states have relevant variations. "
        "If no state-specific amendments are relevant, confirm that the central Acts apply."
    ),
    expected_output=(
        "A summary of state-specific legal variations based on the identified jurisdiction, "
        "or a confirmation that only central legal sections apply."
    ),
    context=[legal_research_task]
)
