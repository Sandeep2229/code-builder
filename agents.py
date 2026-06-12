from langchain_openai import ChatOpenAI
from state import CodeBuilderState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def uiux_agent(state: CodeBuilderState) -> dict:
    print("--- UI/UX Agent Running ---")
    
    feature = state["feature_request"]
    
    response = llm.invoke(
        f"""You are a senior UI/UX designer.
        
Given this feature request: {feature}

Provide a detailed design specification including:
1. Layout and structure
2. Key UI components needed
3. User flow
4. Style guidelines (colors, typography, spacing)
5. Mobile responsiveness notes

Be specific and detailed."""
    )
    
    return {
        "design_spec": response.content,
        "current_stage": "design_complete",
        "status": "in_progress"
    }


def frontend_agent(state: CodeBuilderState) -> dict:
    print("--- Frontend Agent Running ---")
    
    design = state["design_spec"]
    bugs = state.get("bugs_found")
    
    if bugs:
        prompt = f"""You are a senior frontend engineer.
        
Design spec: {design}
Bugs to fix: {bugs}

Fix the bugs and return the complete updated HTML, CSS, and JavaScript code."""
    else:
        prompt = f"""You are a senior frontend engineer.

Design spec: {design}

Write complete HTML, CSS, and JavaScript code that implements this design.
Be specific and write real working code."""
    
    response = llm.invoke(prompt)
    
    return {
        "frontend_code": response.content,
        "current_stage": "frontend_complete",
        "bugs_found": None,
        "status": "in_progress"
    }


def backend_agent(state: CodeBuilderState) -> dict:
    print("--- Backend Agent Running ---")
    
    feature = state["feature_request"]
    frontend = state["frontend_code"]
    bugs = state.get("bugs_found")
    
    if bugs:
        prompt = f"""You are a senior backend engineer.

Feature request: {feature}
Bugs to fix: {bugs}

Fix the bugs and return the complete updated FastAPI backend code."""
    else:
        prompt = f"""You are a senior backend engineer.
        
Feature request: {feature}
Frontend code: {frontend}

Write a complete Python FastAPI backend including:
1. All necessary API endpoints
2. Data models
3. Business logic
4. Error handling

Write real working code."""
    response = llm.invoke(prompt)
    return {
        "backend_code": response.content,
        "current_stage": "backend_complete",
        "bugs_found": None,
        "bug_owner": None,
        "status": "in_progress"
    }



def tester_agent(state: CodeBuilderState) -> dict:
    print("--- Tester Agent Running ---")
    
    frontend = state["frontend_code"]
    backend = state["backend_code"]
    revision_count = state["revision_count"]
    
    response = llm.invoke(
        f"""You are a senior QA engineer.
        
Frontend code: {frontend}
Backend code: {backend}

Review both carefully and determine if there are critical bugs.

Format your response EXACTLY as:
VERDICT: PASS or FAIL
OWNER: frontend or backend (who owns the bug)
BUGS: [describe the bug clearly, or NONE]
TEST_CASES: [list 3 test cases]"""
    )
    
    content = response.content
    verdict = "PASS"
    bugs = None
    owner = None
    
    for line in content.split("\n"):
        if line.startswith("VERDICT:"):
            verdict = line.replace("VERDICT:", "").strip()
        if line.startswith("OWNER:"):
            owner = line.replace("OWNER:", "").strip().lower()
        if line.startswith("BUGS:") and "NONE" not in line:
            bugs = line.replace("BUGS:", "").strip()
    
    if revision_count >= 2:
        verdict = "PASS"
        bugs = None
        owner = None
    
    if verdict == "PASS":
        next_stage = "tests_passed"
    elif owner == "backend":
        next_stage = "backend_bugs_found"
    else:
        next_stage = "frontend_bugs_found"
    
    print(f"--- Tester verdict: {verdict} | Owner: {owner} ---")
    
    return {
        "test_cases": content,
        "bugs_found": bugs,
        "bug_owner": owner,
        "current_stage": next_stage,
        "revision_count": revision_count + 1,
        "status": "done" if verdict == "PASS" else "in_progress"
    }