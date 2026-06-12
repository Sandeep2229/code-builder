# Code Builder

Autonomous multi-agent system that builds full-stack features from a single description.

## Architecture

Four agents coordinate through a shared blackboard with no central orchestrator.

- UI/UX Agent: Produces design specification from feature request
- Frontend Agent: Writes HTML, CSS, and JavaScript from design spec
- Backend Agent: Writes FastAPI backend from feature request and frontend code
- Tester Agent: Reviews both, identifies bugs, and routes to the correct agent for fixes

## Key Design Decisions

- Blackboard pattern: all coordination happens through shared state
- No supervisor agent: routing driven by state values via conditional edges
- Smart bug routing: tester identifies whether bugs belong to frontend or backend
- Full observability: every node execution traced in LangSmith

## How to Run

1. Clone the repo
2. Create a virtual environment and activate it
3. Run pip install langgraph langchain-openai langsmith python-dotenv
4. Add your API keys to a .env file
5. Run python main.py
