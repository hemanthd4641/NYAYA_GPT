# agents/state_law_agent.py

from crewai import Agent
from agents.llm_config import get_smart_llm
from tools.state_law_search_tool import state_law_variations_tool

state_law_agent = Agent(
    role="State Law Researcher",
    goal="Identify specific state-level amendments or variations for legal sections in the user's state.",
    backstory=(
        "You are an expert in the constitutional and administrative variations of Indian law. "
        "You know that while the IPC is a central act, many states have introduced their own "
        "amendments that change punishments or add specific clauses. Your job is to find "
        "if the user's state has any such specific legal variations for the case at hand."
    ),
    tools=[state_law_variations_tool],
    llm=get_smart_llm(temperature=0.2),
    verbose=True,
    allow_delegation=False
)
