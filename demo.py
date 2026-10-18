from typing import TypedDict
import random
import string

from langgraph.graph import StateGraph, END

class ChainState(TypedDict):
    s:str
    n: int

initial_state = ChainState(n = 1, s = "a")
def add(state: ChainState) -> ChainState:
    new_letter = random.choice(string.ascii_lowercase)
    return {**state,"n": state["n"]+1, "s": new_letter}

def print_out(state:ChainState) -> ChainState:
    print ({
        "current n": state["n"], 
        "current letter": state["s"]
           })
    return state

def stop_condition(state: ChainState) ->bool:
    return state["n"] > 12

workflow = StateGraph(ChainState)
workflow.add_node("add", add)
workflow.add_node("print", print_out)

workflow.add_edge("add", "print")

workflow.add_conditional_edges("print", stop_condition, {True: END, False: "add"})

workflow.set_entry_point("add")

app = workflow.compile()


if __name__ == "__main__":
    print(app.invoke(initial_state))