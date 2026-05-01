# crew.py

from crewai import Crew

from agents.case_intake_agent import case_intake_agent
from agents.timeline_agent import timeline_agent
from agents.matchmaker_agent import matchmaker_agent
from agents.legal_research_agent import legal_research_agent
from agents.state_law_agent import state_law_agent
from agents.document_analyst_agent import document_analyst_agent
from agents.legal_procedural_agent import legal_procedural_agent
from agents.case_outcome_agent import case_outcome_agent
from agents.evidence_checklist_agent import evidence_checklist_agent
from agents.legal_precedent_agent import legal_precedent_agent
from agents.legal_drafter_agent import legal_drafter_agent

from tasks.case_intake_task import case_intake_task
from tasks.timeline_task import timeline_task
from tasks.matchmaker_task import matchmaker_task
from tasks.legal_research_task import legal_research_task
from tasks.state_law_task import state_law_task
from tasks.document_analysis_task import document_analysis_task
from tasks.bail_fine_task import bail_fine_task
from tasks.case_outcome_task import case_outcome_task
from tasks.evidence_checklist_task import evidence_checklist_task
from tasks.legal_precedent_task import legal_precedent_task
from tasks.legal_drafter_task import legal_drafter_task


legal_assistant_crew = Crew(
    agents=[
        case_intake_agent,
        timeline_agent,
        matchmaker_agent,
        legal_research_agent,
        state_law_agent,
        document_analyst_agent,
        legal_procedural_agent,
        case_outcome_agent,
        evidence_checklist_agent,
        legal_precedent_agent,
        legal_drafter_agent
    ],
    tasks=[
        case_intake_task,
        timeline_task,
        matchmaker_task,
        legal_research_task,
        state_law_task,
        document_analysis_task,
        bail_fine_task,
        case_outcome_task,
        evidence_checklist_task,
        legal_precedent_task,
        legal_drafter_task
    ],
    verbose=True
)