from typing import Optional
from typing_extensions import TypedDict

class CodeBuilderState(TypedDict):
    # The original feature request
    feature_request: str

    # UI/UX Agent output
    design_spec: Optional[str]

    # Frontend Agent output
    frontend_code: Optional[str]

    # Backend Agent output
    backend_code: Optional[str]

    # Tester Agent output
    test_cases: Optional[str]
    bugs_found: Optional[str]
    bug_owner: Optional[str]

    # System tracking
    current_stage: str
    revision_count: int
    status: str
    routing_table: Optional[dict]

