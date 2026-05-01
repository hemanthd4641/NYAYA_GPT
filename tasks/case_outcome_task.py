# tasks/case_outcome_task.py

from crewai import Task
from agents.case_outcome_agent import case_outcome_agent
from tasks.legal_research_task import legal_research_task
from tasks.bail_fine_task import bail_fine_task

case_outcome_task = Task(
    agent=case_outcome_agent,
    description=(
        "Based on the identified legal sections (from the Multi-Act Research Agent) "
        "and the procedural information (from the Bail & Fine Calculator), "
        "provide a detailed case outcome analysis.\n\n"
        "Your analysis must include:\n"
        "1. **Probability of Success** (as a percentage, e.g., 65%) — estimate how likely "
        "the user is to win this case in court, with reasons.\n"
        "2. **Key Strengthening Factors** — what factors will help the user's case (e.g., "
        "digital evidence, eyewitnesses, CCTV footage).\n"
        "3. **Key Weakening Factors** — what gaps or challenges might hurt the case.\n"
        "4. **Expected Penalty for the Accused** — summarize the likely fine and imprisonment.\n"
        "5. **Realistic Timeline** — estimate how long this type of case typically takes in "
        "Indian courts (e.g., 6 months to 2 years).\n\n"
        "Be honest but empathetic. This is for an ordinary citizen who needs to understand "
        "their situation clearly."
    ),
    expected_output=(
        "A structured Case Outcome Analysis containing:\n"
        "- Probability of Success: XX%\n"
        "- Key Strengths of the Case\n"
        "- Key Weaknesses / Risks\n"
        "- Expected Penalty for the Accused\n"
        "- Realistic Court Timeline\n"
        "- Overall Recommendation"
    ),
    context=[legal_research_task, bail_fine_task]
)
