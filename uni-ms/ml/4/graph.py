# graph.py
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import json
from agents import *
from database import get_value_by_id

def run_model(llm, d: dict) -> str:
    a = llm.invoke(d)
    # import pdb; pdb.set_trace()
    # print("=== ANS: ", a)
    return a

class AgentState(TypedDict):
    query: str
    balancer_choice: int
    search_values: list[int, str]
    thought_text: str

graph_builder = StateGraph(AgentState)

def build_search_context(search_values) -> str:
    if not search_values:
        return ""

    search_context = "Также, вот данные полученные агентом-поисковиком из базы данных (в формате 'ключ - значение'):\n"
    for i in search_values:
        search_context += f"{i[0]} - {i[1]}\n"
    return search_context

def balancer_node(state: AgentState) -> AgentState:
    print("=== balancer_node", end="")
    answer = run_model(balancer_agent, {
        "query": state["query"],
    })

    if answer not in ("1", "2", "3"):
        raise Exception(f"===== ERROR: Cannot determine balancer answer: {choice}")

    return {
        "balancer_choice": int(answer),
    }

# Узлы графа
def simple_node(state: AgentState) -> AgentState:
    print("=== simple_node")
    answer = run_model(simple_agent, {
        "query": state["query"],
    })

    # print("===ANS===")
    # print(answer)
    # print("=========")

def search_node(state: AgentState) -> AgentState:
    answer = run_model(search_agent, {
        "query": state["query"],
    })

    try:
        # Parse list [1, 2, 3]
        print("search_node: ", answer)
        l: list = eval(answer)
    except Exception as e:
        raise Exception(f"===== ERROR: parse search_agent: {answer}")

    search_values = []
    for i in l:
        value = get_value_by_id("2.db", i)
        search_values.append((i, value))

    return {
        "search_values": search_values,
    }

def brain_node(state: AgentState) -> AgentState:
    search_context = build_search_context(state.get("search_values", ""))

    answer = run_model(brain_agent, {
        "query": state["query"],
        "search_context": search_context
    })

    return {
        "thought_text": answer,
    }

def gen_node(state: AgentState) -> AgentState:
    search_context = build_search_context(state.get("search_values", ""))
    thought_context = "Вот мыслительный процесс, произведенный агентом-мыслителем:\n" + state["thought_text"] + "\n"

    answer = run_model(gen_agent, {
        "query": state["query"],
        "search_context": search_context,
        "thought_context": thought_context,
    })

    print("===GEN_ANS===")
    print(answer)
    print("=============")
    
def balancer_next_state(state: AgentState) -> str:
    choice = state["balancer_choice"]
    if choice == 1:
        return "simple"
    if choice == 2:
        return "search"
    if choice == 3:
        return "brain"
    
    return END

# Добавление узлов
graph_builder.add_node("balancer", balancer_node)
graph_builder.add_node("simple", simple_node)
graph_builder.add_node("search", search_node)
graph_builder.add_node("brain", brain_node)
graph_builder.add_node("gen", gen_node)

# Создание графа
graph_builder.set_entry_point("balancer")
graph_builder.add_conditional_edges("balancer", balancer_next_state)
graph_builder.add_edge("search", "brain")
graph_builder.add_edge("brain", "gen")

# Компиляция
graph = graph_builder.compile()
