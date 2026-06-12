from langgraph.graph import StateGraph, END
from state import CodeBuilderState
from agents import uiux_agent, frontend_agent, backend_agent, tester_agent

DEFAULT_ROUTING_TABLE = {
    "design_complete": "frontend",
    "frontend_complete": "backend",
    "backend_complete": "tester",
    "tests_passed": END,
    "frontend_bugs_found": "frontend",
    "backend_bugs_found": "backend"
}

def should_continue(state: CodeBuilderState) -> str:
    stage = state["current_stage"]
    routing_table = state.get("routing_table") or DEFAULT_ROUTING_TABLE
    next_step = routing_table.get(stage, END)
    print(f"--- Routing: {stage} -> {next_step} ---")
    return next_step

def build_graph():
    graph = StateGraph(CodeBuilderState)

    graph.add_node("uiux", uiux_agent)
    graph.add_node("frontend", frontend_agent)
    graph.add_node("backend", backend_agent)
    graph.add_node("tester", tester_agent)

    graph.set_entry_point("uiux")

    graph.add_conditional_edges("uiux", should_continue)
    graph.add_conditional_edges("frontend", should_continue)
    graph.add_conditional_edges("backend", should_continue)
    graph.add_conditional_edges("tester", should_continue)

    return graph.compile()