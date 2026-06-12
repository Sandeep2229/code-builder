import os
from dotenv import load_dotenv
from graph import build_graph

load_dotenv()

def run_code_builder(feature_request: str):
    graph = build_graph()

    initial_state = {
        "feature_request": feature_request,
        "design_spec": None,
        "frontend_code": None,
        "backend_code": None,
        "test_cases": None,
        "bugs_found": None,
        "current_stage": "start",
        "revision_count": 0,
        "status": "in_progress",
        "routing_table": None
    }

    print("\n=== Code Builder System Starting ===\n")

    result = graph.invoke(initial_state)

    print("\n=== DESIGN SPEC ===")
    print(result["design_spec"])
    
    print("\n=== FRONTEND CODE ===")
    print(result["frontend_code"])
    
    print("\n=== BACKEND CODE ===")
    print(result["backend_code"])
    
    print("\n=== TEST CASES ===")
    print(result["test_cases"])
    
    print("\n=== STATUS:", result["status"], "===")

if __name__ == "__main__":
    run_code_builder(
        "Build a login page with email and password authentication"
    )