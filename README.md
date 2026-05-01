<div align="center">

<img src="https://img.shields.io/badge/⚖️%20AI%20Legal%20Assistant-Legal%20Intelligence%20Platform-4B0082?style=for-the-badge" alt="AI Legal Assistant"/>

# ⚖️ Personal AI Legal Assistant
### *A Multi-Agent Legal Intelligence Platform for Indian Law*

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Chat%20UI-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-8B5CF6?style=flat-square)](https://crewai.com/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.1-F97316?style=flat-square)](https://groq.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Search-22C55E?style=flat-square)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

**An AI-powered legal research platform that combines 11 specialized agents, 6 Indian law databases, voice input, document auditing, and a ChatGPT-style interface — all in one tool.**

[🚀 Features](#-features) · [🏛️ Architecture](#-architecture) · [🤖 Meet the Agents](#-meet-the-agents) · [📚 Legal Acts](#-supported-legal-acts) · [⚙️ Setup](#-setup) · [🖥️ Usage](#-usage)

---

</div>

## 🌟 Overview

The **Personal AI Legal Assistant** is a production-grade, conversational legal platform built for Indian citizens. Instead of a single chatbot, it deploys a **crew of 11 specialized AI agents** — each an expert in a different area of law — to analyze your case from every angle and produce a comprehensive legal report.

Whether you are filing an FIR, auditing a contract, researching cybercrime laws, or understanding your bail rights, this platform has you covered.

---

## 🚀 Features

### 💬 ChatGPT-Style Conversational Interface
- Natural multi-turn legal conversations
- Full **chat history** saved to a local SQLite database
- Browse, reload, and delete past conversations from the sidebar
- Fresh, clean session on every new browser visit
- **➕ New Chat** button for instant new conversations

### 🎤 Voice-to-Legal-Query
- **Record your legal question** using the built-in microphone
- Powered by **Groq Whisper** for fast, accurate transcription
- Voice input is seamlessly added to the chat pipeline

### 📁 Document & Image Intelligence
| Capability | Description |
|---|---|
| **PDF Analysis** | Upload contracts, FIRs, or notices — text is extracted and analyzed |
| **Image/Evidence** | Upload photos of evidence or handwritten notes |
| **Vision AI** | Uses **Groq LLaMA Vision** to "read" and describe image content |
| **Document Audit** | Scans documents for loopholes and missing clauses |

### ⚖️ Multi-Act Legal Research (RAG)
The core engine searches across **6 dedicated Indian Law databases simultaneously**:

| Act | Focus Area |
|---|---|
| 📕 **IPC** (Indian Penal Code) | Core criminal offenses |
| 📗 **CrPC** (Code of Criminal Procedure) | Arrest, bail & trial procedures |
| 📘 **Indian Evidence Act (IEA)** | Digital & physical evidence rules |
| 💻 **IT Act, 2000** | Hacking, cybercrime, online fraud |
| 👶 **POCSO Act, 2012** | Protection of children from sexual offenses |
| 🛍️ **Consumer Protection Act, 2019** | Product defects & service complaints |

### 🧮 Bail & Fine Calculator
- Automatically identifies if your offense is **Bailable or Non-Bailable**
- Calculates **Maximum Imprisonment** and **Fine Range** per section
- Provides a clear **Procedural Outlook** in the final report

### 🔮 Predictive Case Outcome Analysis
- Estimates the **Probability of Success** for the user's case based on identified legal sections.
- Highlights key **strengths** and **weaknesses/risks** in the current scenario.
- Provides realistic timelines for court proceedings in India.

### ✅ Court-Ready Evidence Checklist
- Generates a personalized checklist of documents, digital artifacts, and physical evidence required.
- Separates evidence into categories: Official Documents, Financial Records, Witness Info, etc.
- Provides **Immediate Action Items** to protect the case.

### 🗺️ State-Specific Law Support
- Detects your **State/UT** from natural conversation
- Finds **local amendments** that differ from central laws
- Examples: Haryana's Snatching Amendment, Maharashtra's Medical Negligence rules

### 📄 Professional PDF Export
- **One-click download** of a complete legal report
- Includes: Header, Timeline, Applicable Sections, Procedural Outlook, Audit Summary
- Unicode-safe rendering for all Indian legal symbols (₹, §, etc.)

### 🔍 Precedent Research
- Live web search via **Tavily API** for real Indian court cases
- Finds case titles, summaries, and links to full judgments from **IndianKanoon**

---

## 🏛️ Architecture

```
User Query (Text / Voice / Document)
          │
          ▼
┌─────────────────────────────────────┐
│      Streamlit Chat Interface       │
│  (ChatGPT UI + SQLite History)      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                  CrewAI Orchestrator                │
│  (9 Agents running in a sequential pipeline)        │
└──────┬──────────────────────────────────────────────┘
       │
       ├─► 1. Case Intake Agent
       ├─► 2. Legal Chronologist (Timeline)
       ├─► 3. Lawyer Matchmaker
       ├─► 4. Multi-Act Legal Researcher ──► ChromaDB (6 Collections)
       ├─► 5. State Law Researcher ──────► Tavily Web Search
       ├─► 6. Legal Document Auditor
       ├─► 7. Procedural Expert (Bail & Fine)
       ├─► 8. Case Outcome Predictor
       ├─► 9. Evidence Checklist Specialist
       ├─► 10. Legal Precedent Agent ────► Tavily Web Search
       └─► 11. Legal Drafter (Final Report)
                    │
                    ▼
           ┌────────────────┐
           │  PDF Download  │
           │  Chat History  │
           └────────────────┘
```

---

## 🤖 Meet the Agents

| # | Agent | Role | Tools |
|---|---|---|---|
| 1 | **Case Intake Agent** | Classifies the legal issue and extracts key facts | — |
| 2 | **Legal Chronologist** | Extracts dates and builds a case timeline | — |
| 3 | **Lawyer Matchmaker** | Recommends the right type of legal specialist | — |
| 4 | **Multi-Act Legal Researcher** | Searches all 6 law databases simultaneously | ChromaDB RAG |
| 5 | **State Law Researcher** | Finds state-specific amendments and variations | Tavily Search |
| 6 | **Legal Document Auditor** | Scans uploaded documents for loopholes | Vision AI |
| 7 | **Procedural Law Expert** | Calculates bail status, fines & imprisonment | ChromaDB RAG |
| 8 | **Case Outcome Predictor** | Estimates success probability and timelines | — |
| 9 | **Evidence Checklist Specialist** | Builds a personalized court evidence list | — |
| 10 | **Legal Precedent Agent** | Searches for real court case precedents | Tavily Search |
| 11 | **Legal Drafter** | Compiles everything into a formal legal document | — |

---

## 📚 Supported Legal Acts

The platform ships with complete vector databases for all major Indian laws:

```
chroma_vectordb/
├── ipc_collection/          # 511+ sections of IPC
├── crpc_collection/         # Code of Criminal Procedure
├── iea_collection/          # Indian Evidence Act
├── it_act_collection/       # Information Technology Act, 2000
├── pocso_collection/        # POCSO Act, 2012
└── consumer_collection/     # Consumer Protection Act, 2019
```

---

## ⚙️ Setup

### Prerequisites
- Python 3.11+
- A [Groq API Key](https://console.groq.com/) (Free tier available)
- A [Tavily API Key](https://tavily.com/) (Free tier available)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-legal-assistant.git
cd ai-legal-assistant/ai-legal-assistant-crewai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
PERSIST_DIRECTORY_PATH=./chroma_vectordb
```

### 4. Build the Legal Vector Databases
```bash
python legal_vectordb_builder.py
```
> ⏳ This downloads the embedding model and indexes all 6 law collections. Only needed once.

### 5. Run the Application
```bash
python run_app.py
```
Open your browser at **http://localhost:8501** 🎉

---

## 🖥️ Usage

### Ask a Legal Question
```
"My laptop was hacked and money was stolen from my bank in Maharashtra. 
What are my legal options?"
```
The assistant will automatically:
- Find relevant **IT Act** sections (hacking)
- Find relevant **IPC** sections (theft/fraud)
- Check **Maharashtra-specific** amendments
- Calculate your **bail eligibility**
- Search for **similar court cases**
- Generate a complete **FIR draft**

### Upload a Document for Audit
1. Click **"📁 Documents & Evidence"** in the sidebar
2. Upload a contract, notice, or existing FIR
3. Ask: `"Find loopholes in this contract"`

### Use Voice Input
1. Click **"🎤 Record"**
2. Speak your legal issue
3. The system transcribes and processes it automatically

### Download the Legal Report
After any analysis, click **"📥 Download Official Legal Report (PDF)"**

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit (ChatGPT-style UI) |
| **Agent Orchestration** | CrewAI |
| **LLM** | Groq LLaMA 3.1 8B Instant |
| **Vector Database** | ChromaDB |
| **Embeddings** | Sentence-Transformers (all-mpnet-base-v2) |
| **Web Search** | Tavily API |
| **PDF Generation** | fpdf2 |
| **Voice Input** | Groq Whisper via streamlit-mic-recorder |
| **Chat History** | SQLite (local, persistent) |
| **Document Parsing** | PyPDF2 |

---

## 📁 Project Structure

```
ai-legal-assistant-crewai/
├── app.py                      # Main Streamlit application
├── crew.py                     # CrewAI crew definition
├── run_app.py                  # Application launcher
├── legal_vectordb_builder.py   # Builds ChromaDB collections
├── .env                        # API keys (not committed)
│
├── agents/                     # 9 Specialized AI Agents
│   ├── llm_config.py
│   ├── case_intake_agent.py
│   ├── timeline_agent.py
│   ├── matchmaker_agent.py
│   ├── legal_research_agent.py
│   ├── state_law_agent.py
│   ├── document_analyst_agent.py
│   ├── legal_procedural_agent.py
│   ├── case_outcome_agent.py
│   ├── evidence_checklist_agent.py
│   ├── legal_precedent_agent.py
│   └── legal_drafter_agent.py
│
├── tasks/                      # Agent Task Definitions
│   ├── case_intake_task.py
│   ├── timeline_task.py
│   ├── matchmaker_task.py
│   ├── legal_research_task.py
│   ├── state_law_task.py
│   ├── document_analysis_task.py
│   ├── bail_fine_task.py
│   ├── case_outcome_task.py
│   ├── evidence_checklist_task.py
│   ├── legal_precedent_task.py
│   └── legal_drafter_task.py
│
├── tools/                      # Helper Tools & Utilities
│   ├── legal_search_tool.py
│   ├── legal_precedent_search_tool.py
│   ├── file_processor.py
│   ├── pdf_generator.py
│   ├── voice_handler.py
│   └── history_manager.py
│
└── *.json                      # Legal Act Databases
    ├── ipc.json
    ├── crpc.json
    ├── iea.json
    ├── it_act.json
    ├── pocso.json
    └── consumer_act.json
```

---

## ⚠️ Disclaimer

> This tool is for **educational and informational purposes only**. It does not constitute professional legal advice. Always consult a qualified lawyer for your specific legal situation.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using CrewAI, Groq, and ChromaDB**

*Making legal knowledge accessible to everyone in India*

</div>