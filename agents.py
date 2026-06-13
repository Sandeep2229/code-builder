from langchain_openai import ChatOpenAI
from state import CodeBuilderState


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def reflect(state: CodeBuilderState, agent_name: str) -> list:
    bugs = state.get("bugs_found")
    revision = state.get("revision_count", 0)
    previous_log = state.get("reasoning_log") or []

    response = llm.invoke(
        f"""You are a self-reflective AI agent named {agent_name}.

A bug was found in your code:
{bugs}

Previous reasoning log:
{previous_log}

Ask yourself:
1. Why did this bug happen?
2. What assumption did I make that was wrong?
3. What will I do differently this time?

Write a short reasoning note. Be specific."""
    )

    entry = {
        "agent": agent_name,
        "revision": revision,
        "reasoning": response.content
    }
    print(f"\n--- [{agent_name}] REASONING (Revision {revision}) ---")
    print(response.content)
    print("---------------------------------------------------\n")

    return previous_log + [entry]




def uiux_agent(state: CodeBuilderState) -> dict:
    print("--- UI/UX Agent Running ---")
    
    feature = state["feature_request"]
    bugs = state.get("bugs_found")
    
    if bugs:
        reasoning_log = reflect(state, "uiux_agent")
        prompt = f"""You are a senior UI/UX designer.

Feature request: {feature}
Bugs to fix: {bugs}

Your reasoning about why this bug happened:
{reasoning_log[-1]['reasoning']}

Use that reasoning to fix the design spec and return the complete updated design specification."""
    else:
        reasoning_log = state.get("reasoning_log") or []
        prompt = f"""You are a senior UI/UX designer.

Given this feature request: {feature}

Provide a detailed design specification including:
1. Layout and structure
2. Key UI components needed
3. User flow
4. Style guidelines (colors, typography, spacing)
5. Mobile responsiveness notes

Be specific and detailed."""
    
    response = llm.invoke(prompt)
    
    return {
        "design_spec": response.content,
        "current_stage": "design_complete",
        "bugs_found": None,
        "reasoning_log": reasoning_log,
        "status": "in_progress"
    }


def frontend_agent(state: CodeBuilderState) -> dict:
    print("--- Frontend Agent Running ---")
    
    design = state["design_spec"]
    bugs = state.get("bugs_found")
    
    if bugs:
        reasoning_log = reflect(state, "frontend_agent")
        prompt = f"""You are a senior frontend engineer.

Design spec: {design}
Bugs to fix: {bugs}

Your reasoning about why this bug happened:
{reasoning_log[-1]['reasoning']}

Use that reasoning to fix the bugs and return the complete updated HTML, CSS, and JavaScript code."""
    else:
        reasoning_log = state.get("reasoning_log") or []
        prompt = f"""You are a senior frontend engineer.

Design spec: {design}

Write complete HTML, CSS, and JavaScript code that implements this design.
Be specific and write real working code."""
    
    response = llm.invoke(prompt)
    
    return {
        "frontend_code": response.content,
        "current_stage": "frontend_complete",
        "bugs_found": None,
        "reasoning_log": reasoning_log,
        "status": "in_progress"
    }


def backend_agent(state: CodeBuilderState) -> dict:
    print("--- Backend Agent Running ---")
    
    feature = state["feature_request"]
    frontend = state["frontend_code"]
    bugs = state.get("bugs_found")
    
    if bugs:
        reasoning_log = reflect(state, "backend_agent")
        prompt = f"""You are a senior backend engineer.

Feature request: {feature}
Bugs to fix: {bugs}

Your reasoning about why this bug happened:
{reasoning_log[-1]['reasoning']}

Use that reasoning to fix the bugs and return the complete updated FastAPI backend code."""
    else:
        reasoning_log = state.get("reasoning_log") or []
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
        "reasoning_log": reasoning_log,
        "status": "in_progress"
    }



def tester_agent(state: CodeBuilderState) -> dict:
    print("--- Tester Agent Running ---")
    
    design = state["design_spec"]
    frontend = state["frontend_code"]
    backend = state["backend_code"]
    revision_count = state["revision_count"]
    
    response = llm.invoke(
        f"""You are a senior QA engineer.

Design spec: {design}
Frontend code: {frontend}
Backend code: {backend}

Review all three carefully and determine if there are critical bugs.

Format your response EXACTLY as:
VERDICT: PASS or FAIL
OWNER: frontend or backend or uiux (who owns the bug)
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
    elif owner == "uiux":
        next_stage = "uiux_bugs_found"
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