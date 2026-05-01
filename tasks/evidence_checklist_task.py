# tasks/evidence_checklist_task.py

from crewai import Task
from agents.evidence_checklist_agent import evidence_checklist_agent
from tasks.case_intake_task import case_intake_task
from tasks.legal_research_task import legal_research_task

evidence_checklist_task = Task(
    agent=evidence_checklist_agent,
    description=(
        "Based on the case facts (from Case Intake) and the applicable legal sections "
        "(from the Legal Research Agent), generate a court-ready evidence checklist.\n\n"
        "The checklist must be specific to THIS case, not generic. Organize it into:\n\n"
        "📄 **Official Documents Required**\n"
        "List all government or legal documents the user must gather "
        "(e.g., FIR copy, Sale Deed, Aadhar Card, Bank Statements, Death Certificate).\n\n"
        "🏦 **Financial Records**\n"
        "List any financial evidence relevant to this case "
        "(e.g., transaction history, rent receipts, insurance documents).\n\n"
        "💻 **Digital Evidence**\n"
        "For cyber or fraud cases, list what digital proof must be preserved "
        "(e.g., screenshots of messages, email threads, call logs, website URLs).\n\n"
        "👥 **Witness Information**\n"
        "Describe the type of witnesses the user should identify and what their statement "
        "should cover (e.g., neighbours, CCTV operators, colleagues).\n\n"
        "📸 **Physical Evidence**\n"
        "List any physical items that should be secured "
        "(e.g., CCTV footage, damaged property, medical reports).\n\n"
        "⚡ **Immediate Action Items**\n"
        "List 3-5 things the user must do RIGHT NOW to protect their case "
        "(e.g., 'File FIR within 24 hours', 'Do not delete WhatsApp messages')."
    ),
    expected_output=(
        "A personalized, categorized 'Court-Ready Evidence Checklist' with specific items "
        "under each category and immediate action steps the user must take."
    ),
    context=[case_intake_task, legal_research_task]
)
