# legal_drafter_task.py

from crewai import Task

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

legal_drafter_task = Task(
    agent=legal_drafter_agent,
    description=(
        "You are the final agent. Compile all the findings from the previous agents into a single, "
        "comprehensive legal document. The document should include:\n\n"
        "1. **Case Summary** — Brief description of the issue.\n"
        "2. **Timeline of Events** — From the Chronologist.\n"
        "3. **Applicable Legal Sections** — From multiple Acts (IPC, IT Act, CrPC, etc.).\n"
        "4. **State-Specific Amendments** — If applicable.\n"
        "5. **Document Audit Summary** — Loopholes or missing clauses (if a document was uploaded).\n"
        "6. **Procedural Outlook** — Bail status, punishment range, and fine estimates.\n"
        "7. **Case Outcome Prediction** — Probability of success and key factors.\n"
        "8. **Court-Ready Evidence Checklist** — What the user must collect.\n"
        "9. **Recommended Lawyer Type** — From the Matchmaker.\n"
        "10. **Relevant Precedents** — Similar past court cases.\n"
        "11. **Formal Legal Draft** — An FIR or Legal Notice the user can submit. **IMPORTANT**: Avoid excessive repetition of witness signatures or verification blocks. Provide at most two witness slots if necessary. Do not repeat the same verification statement multiple times.\n\n"
        "Write this in a formal, professional, and empathetic tone suitable for a lay person to understand."
    ),
    expected_output=(
        "A complete legal report with all 11 sections clearly separated and labeled."
    ),
    context=[
        case_intake_task, timeline_task, matchmaker_task,
        legal_research_task, state_law_task, document_analysis_task,
        bail_fine_task, case_outcome_task, evidence_checklist_task,
        legal_precedent_task
    ]
)
