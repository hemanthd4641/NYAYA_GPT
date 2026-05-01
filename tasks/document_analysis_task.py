# tasks/document_analysis_task.py

from crewai import Task
from agents.document_analyst_agent import document_analyst_agent
from tasks.legal_research_task import legal_research_task
from tasks.state_law_task import state_law_task

document_analysis_task = Task(
    agent=document_analyst_agent,
    description=(
        "Analyze the provided user input and any extracted file contents (documents/images) "
        "if they represent an existing legal document like a contract, notice, or FIR.\n\n"
        "1. Compare the document against the identified legal sections and state laws.\n"
        "2. Identify potential loopholes (vague wording, missing definitions).\n"
        "3. Identify missing clauses that would protect the user (e.g., Termination, Liability, Jurisdiction).\n"
        "4. Flag any inconsistencies with the reported facts."
    ),
    expected_output=(
        "A detailed 'Document Audit Report' highlighting Loopholes, Missing Clauses, "
        "and Legal Risks. If no existing document was provided, simply state 'No document analysis required'."
    ),
    context=[legal_research_task, state_law_task]
)
