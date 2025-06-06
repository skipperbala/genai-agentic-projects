# core/langgraph_runner.py

from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.character_agent import character_agent
from agents.plot_manager import plot_agent
from agents.world_builder import world_agent


# Define state object for the story flow
class StoryState(TypedDict):
    user_input: str
    plot_context: str
    world_context: str
    character_output: str


# Character agent step
def run_character(state: StoryState) -> StoryState:
    response = character_agent(state["user_input"], state["plot_context"], state["world_context"])
    state["character_output"] = response
    return state


# Plot manager step
def run_plot(state: StoryState) -> StoryState:
    plot_update = plot_agent(state["user_input"])
    state["plot_context"] = plot_update
    return state


# World builder step
def run_world(state: StoryState) -> StoryState:
    world_update = world_agent(state["user_input"])
    state["world_context"] = world_update
    return state


# LangGraph pipeline setup
def build_story_graph():
    builder = StateGraph(StoryState)

    builder.add_node("plot_agent", run_plot)
    builder.add_node("world_agent", run_world)
    builder.add_node("character_agent", run_character)

    builder.set_entry_point("plot_agent")

    builder.add_edge("plot_agent", "world_agent")
    builder.add_edge("world_agent", "character_agent")
    builder.add_edge("character_agent", END)

    return builder.compile()
