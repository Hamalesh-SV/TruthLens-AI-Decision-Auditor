TruthLens — AI Business Decision Auditor

========================================



TruthLens is an AI-powered enterprise fact-checking application designed to enforce decision quality, financial controls, and policy consistency. It audits proposed management memos against internal SQL databases, corporate policy manuals, and meeting transcripts to automatically flag unsupported claims, conflicting financial figures, and missing evidence before decisions are finalized.



BUSINESS VALUE

--------------

* Decision Quality: Prevents executives from executing plans based on false premises by cross-checking claims and generating an automated Assurance Score.

* Financial Controls: Text-to-SQL agents strictly verify budget requests and revenue metrics against structured ground-truth data.

* Project Delivery & Policy Consistency: RAG agents audit resource allocation and proposed actions against official board meeting transcripts and corporate policy manuals.



ARCHITECTURE & TECH STACK

-------------------------

* Orchestration: LangGraph (StateGraph multi-agent workflow)

* LLM Engine: Ollama (Local deployment for privacy: llama3.1:8b, nomic-embed-text)

* Frameworks: LangChain, Langchain-Ollama

* Frontend: Streamlit

* Databases: SQLite (Structured metrics), ChromaDB (Unstructured vector store)

* Ingestion: PyPDF, LangChain TextSplitters



AGENT WORKFLOW

--------------

1. Extractor Node: Decomposes raw memos into atomic, testable claims (metric, policy, meeting_decision).

2. SQL Node: Translates quantitative claims into queries against company_metrics.db.

3. RAG Node: Retrieves semantic context from chroma_db for qualitative claims.

4. Judge Node: Evaluates the original claims against the retrieved internal evidence.

5. Synthesizer Node: Computes the Assurance Score and formats the executive summary.



PROJECT STRUCTURE

-----------------

truthlens/

├── app/                  # Streamlit UI & modular components

├── data/                 # SQLite DB, Chroma DB, and Raw Documents (PDFs, TXT)

├── src/                  

│   ├── agents/           # LangGraph nodes (Extractor, SQL, RAG, Judge, Synthesizer)

│   ├── graph/            # Workflow compiler (workflow.py)

│   ├── ingestion/        # Document loaders and Vector DB seeders

│   └── schemas/          # Pydantic models & Graph State definitions

└── tests/                # Pytest validation scripts



INSTALLATION & SETUP

--------------------

1. Prerequisites

Ensure you have Python 3.10+ and Ollama (https://ollama.com/) installed on your system.



2. Environment Setup

# Create and activate a virtual environment

python -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate



# Install dependencies

pip install -r requirements.txt

pip install langchain-ollama pypdf  # Additional integrations



3. Start Local LLMs

Ensure the Ollama application is running in the background, then pull the required models:

ollama pull llama3.1:8b

ollama pull nomic-embed-text



4. Seed Ground-Truth Databases

Before running the auditor, you must populate the local databases with the company's records.



Seed the SQL Database:

python data/sql_db/seed_database.py



Ingest RAG Documents (PDFs & TXTs):

Ensure your raw company documents are placed inside data/raw_documents/reports/ and data/raw_documents/meetings/, then run:

python src/ingestion/vector_store.py



RUNNING THE APPLICATION

-----------------------

Launch the Streamlit dashboard from the root directory:

streamlit run app/main.py



The application will open in your browser at http://localhost:8501.



DEMO TEST CASE

--------------

Paste the following memo into the text area and click "Run TruthLens Decision Audit":



"Our Q3 Revenue reached $4.2M, which is a strong milestone. However, to address recent issues, we are authorizing Account Executives to offer a 20% automatic renewal discount to at-risk clients without CFO review. Furthermore, as per the October 15 board meeting, we are moving forward with deploying a 2-engineer Customer Reliability Tiger Team with a $50,000 budget."



Expected Output:

* Verified: Q3 Revenue is $4.2M (Found in SQL)

* Verified: 2-engineer Tiger Team (Found in Meeting TXT)

* Refuted: 20% discount (Policy PDF caps at 15%)

* Refuted: $50,000 budget (Meeting TXT caps at $40,000)



TESTING

-------

Run the Pytest suite to validate the LangGraph agent logic without launching the UI:

pytest tests/