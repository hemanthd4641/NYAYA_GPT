# agents/legal_procedural_agent.py

from crewai import Agent
from agents.llm_config import get_llm

legal_procedural_agent = Agent(
    role="Procedural Law Expert",
    goal="Calculate potential punishments, fines, and bail eligibility for the user's case.",
    backstory=(
        "You are an expert in the Code of Criminal Procedure (CrPC) and sentencing guidelines. "
        "You can look at multiple legal sections and determine the overall procedural impact. "
        "You calculate the range of fines and specify if the user is likely to be granted "
        "bail based on the nature of the offenses (Bailable vs Non-Bailable)."
    ),
    llm=get_llm(temperature=0.1),
    verbose=True,
    allow_delegation=False
)
