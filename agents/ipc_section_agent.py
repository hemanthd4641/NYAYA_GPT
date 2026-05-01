# ipc_section_agent.py
# LEGACY: This agent is replaced by legal_research_agent.py but kept for backward compatibility.

from crewai import Agent
from agents.llm_config import get_llm
from tools.ipc_sections_search_tool import search_ipc_sections

ipc_section_agent = Agent(
    role="IPC Section Agent",
    goal="Identify the most relevant Indian Penal Code (IPC) sections based on the legal issue provided.",
    backstory=(
        "You're a seasoned legal researcher with deep knowledge of Indian penal laws. "
        "You specialize in mapping legal issues to applicable IPC sections with precision and clarity. "
        "Your insight helps lawyers and assistants quickly understand the statutory basis of a case."
    ),
    tools=[search_ipc_sections],
    llm=get_llm(temperature=0.3),
    verbose=True,
)
