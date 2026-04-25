# Grid07 AI Assessment

### Setup

1.Clone the repository
2.Create virtual environment: python -m venv venv
3.Activate it: venv\Scripts\actiavte
4.Install libraries: pip install -r requirments.txt
5.Copy .env.example to .env and add your Groq API key

## How to run 

Phase 1: Python phase1.py
Phase 2: python phase2.py
Phase 3: python phase3.py

## Phase 1 - Vector Based Persona Matching

Converts bot personalities into vectors using sentance transformers.
Uese ChromDB to store and search vectors by cosine similarity.
Routes incoming posts to bots whose personality matches the post topic.

Threshold is set to 0.20 instead of assessment's 0.85 because
all-MiniLM-L6-V2produces similarity score in the 0.2 - 0.5 range.
The assessment explicitly says to tweak threshold based on embedding model.

## Phase 2 - LangGraph Content Engine

Three node graph:
-Node 1: Bot descide what topic to search based on its personality
-Node 2: Mock search returns relevent news headlines
-Node 3: Bot writes  opinionated 280 character post using headlines as context

Output is strict JSON with bot_id,topic, and post_content fields.

## Phase 3 - Combat Engine with RAG

Bot reads full thread history as context before replying.
This stimulates RAG where the thread itself is the retrieved context.
In production, threads would be fetched from a database.

Prompt Injection Defense uses three layers:
- Layer 1: System prompt declares bot identity as permanent and unchangeable
- Layer 2: Human input is labeled as UNTRUSTED USER INPUT
- Layer 3: Bot is told exactly what to do when injection is detetced - Keep arguing

## Tech Stack 

- senatnce-transformers: local text embedding
- ChromaDB: vector database
- Groq API: LLM (llama-3.3-70b-versatile)
- LangGraph: multi step AI workflow
- LangChain: LLM interface 

