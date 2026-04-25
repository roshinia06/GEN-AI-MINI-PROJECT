from langgraph.graph import StateGraph
from typing import TypedDict, List

from agents.mode_agent import mode_agent
from agents.retrieval_agent import retrieval_agent
from agents.planner_agent import planner_agent
from agents.budget_agent import budget_agent
from agents.validator_agent import validator_agent
from agents.formatter_agent import formatter_agent


class WorkflowState(TypedDict):
    # Trip parameters
    starting_place: str
    destination: str
    budget: int
    days: int
    mode: str
    people_count: int
    interests: List[str]
    accommodation_type: str
    notes: str

    # Runtime data
    currency_symbol: str
    constraints: str
    context: str
    flight_cost_estimate: int

    # Agent outputs
    plan: dict
    filtered_plan: dict
    final_plan: dict
    validation_errors: list


def run_workflow(
    destination: str,
    budget: int,
    days: int,
    currency_symbol: str = "₹",
    starting_place: str = "Your location",
    mode: str = "seasonal",
    people_count: int = 1,
    interests: List[str] = None,
    accommodation_type: str = "Mid-range",
    notes: str = "",
) -> dict:
    """
    Runs the 6-agent LangGraph workflow and returns the final formatted plan.
    Agent order: mode → retriever → planner → budget → validator → formatter
    """
    graph = StateGraph(WorkflowState)

    # Register nodes
    graph.add_node("mode", mode_agent)
    graph.add_node("retriever", retrieval_agent)
    graph.add_node("planner", planner_agent)
    graph.add_node("budget", budget_agent)
    graph.add_node("validator", validator_agent)
    graph.add_node("formatter", formatter_agent)

    # Define flow
    graph.set_entry_point("mode")
    graph.add_edge("mode", "retriever")
    graph.add_edge("retriever", "planner")
    graph.add_edge("planner", "budget")
    graph.add_edge("budget", "validator")
    graph.add_edge("validator", "formatter")

    app = graph.compile()

    # Build initial state
    initial_state: WorkflowState = {
        "starting_place": starting_place,
        "destination": destination,
        "budget": budget,
        "days": days,
        "currency_symbol": currency_symbol,
        "mode": mode,
        "people_count": people_count,
        "interests": interests or [],
        "accommodation_type": accommodation_type,
        "notes": notes,
        "constraints": "",
        "context": "",
        "flight_cost_estimate": 0,
        "validation_errors": [],
    }

    result = app.invoke(initial_state)
    return result["final_plan"]
