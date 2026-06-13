# Code Builder
Autonomous multi-agent system that builds full-stack features from a single description.

## Architecture
Four agents coordinate through a shared blackboard with no central orchestrator.

- UI/UX Agent: Produces design specification from feature request
- Frontend Agent: Writes HTML, CSS, and JavaScript from design spec
- Backend Agent: Writes FastAPI backend from feature request and frontend code
- Tester Agent: Reviews all three, identifies bugs, and routes to the correct agent for fixes

## Key Design Decisions
- Blackboard pattern: all coordination happens through shared state
- No supervisor agent: routing driven by state values via conditional edges
- Smart bug routing: tester identifies whether bugs belong to frontend, backend, or uiux
- Full observability: every node execution traced in LangSmith

## Self-Healing Agents
When a bug is returned to an agent, it does not fix it blindly. It first calls a reflect function that asks three questions: why did this bug happen, what assumption was wrong, and what will I do differently. The reasoning is written to the blackboard as a structured log with the agent name, revision number, and reasoning text. The agent then uses that reasoning in its next prompt before writing the fix. This prevents the same mistake from being repeated across revision cycles. The reasoning log is invisible to the end user but fully visible in LangSmith traces.

## How to Run
1. Clone the repo
2. Create a virtual environment and activate it
3. Run pip install langgraph langchain-openai langsmith python-dotenv
4. Add your API keys to a .env file
5. Run python main.py
