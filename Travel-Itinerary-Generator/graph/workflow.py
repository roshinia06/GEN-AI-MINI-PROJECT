from langgraph.graph import StateGraph
from typing import TypedDict

from agents.planner_agent import planner_agent
from agents.retrieval_agent import retrieval_agent
from agents.budget_agent import budget_agent
from agents.validator_agent import validator_agent
from agents.mode_agent import mode_agent
from agents.formatter_agent import formatter_agent


class WorkflowState(TypedDict):
    starting_place: str
    destination: str
    budget: int
    days: int
    plan: dict
    context: str
    filtered_plan: dict
    final_plan: dict
    currency_symbol: str
    mode: str
    constraints: str
    validation_errors: list
    people_count: int


def run_workflow(destination, budget, days, currency_symbol="₹", starting_place="Your location", mode="seasonal", people_count=1):

    graph = StateGraph(WorkflowState)

    # Add nodes
    graph.add_node("mode", mode_agent)
    graph.add_node("planner", planner_agent)
    graph.add_node("retriever", retrieval_agent)
    graph.add_node("budget", budget_agent)
    graph.add_node("validator", validator_agent)
    graph.add_node("formatter", formatter_agent)

    # Entry point
    graph.set_entry_point("mode")

    # Flow
    graph.add_edge("mode", "retriever")
    graph.add_edge("retriever", "planner")
    graph.add_edge("planner", "budget")
    graph.add_edge("budget", "validator")
    graph.add_edge("validator", "formatter")

    app = graph.compile()

    # Initial state
    state = {
        "starting_place": starting_place,
        "destination": destination,
        "budget": budget,
        "days": days,
        "currency_symbol": currency_symbol,
        "mode": mode,
        "people_count": people_count,
        "constraints": "",
        "validation_errors": []
    }

    result = app.invoke(state)

    return result["final_plan"]
