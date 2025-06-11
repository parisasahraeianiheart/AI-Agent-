# AI-Agent-
# OSINT AI Agent

This project is a production-grade multi-agent OSINT (Open-Source Intelligence) AI system using LangGraph and Claude Sonnet 4.

## Features
- 🔍 Structured Query Analysis
- 📋 Multi-source OSINT Planning
- 🌐 Retrieval from LinkedIn, Google, Semantic Scholar, etc.
- 🧠 Report synthesis using Claude Sonnet
- 🪢 LangGraph orchestration with memory and feedback

## Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/parisasahraeianiheart/AI-Agent-.git
cd AI-Agent-



osint-ai-agent/
│
├── agents/
│   └── # place your agent files like planning_agent.py, retrieval_agent.py, etc.
│
├── retrieval_sources/
│   └── # place source scrapers like linkedin.py, twitter.py, opencorporates.py, etc.
│
├── prompts/
│   └── # optional: store prompt templates if you split them out
│
├── .gitignore
├── README.md
├── requirements.txt
├── osint_graph.py
├── test_graph.py
├── main.py
├── osint_pipeline.py
├── osint_state.py
├── run_graph.py
