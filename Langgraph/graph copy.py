from langfuse import Langfuse
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
from dotenv import load_dotenv
from langfuse.decorators import observe
from langfuse.openai import openai
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("Gemini_API")

client = openai.Client(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


# response = client.chat.completions.create(
#     model="gemini-1.5-flash",
#     messages={ 'role': 'user', 'content': "hello" }
# )

# answer = response.choices[0].message.content
# print(answer)


class State(TypedDict):
    user_message: str
    ai_message: str
    is_coding_question: bool

@observe()
def detect_user_query(state: State):
    user_message = state.get("user_message")

    # OpenAi call

    state["is_coding_question"] = True
    return state

@observe()
def route(state: State) -> Literal['solve_coding_question', 'solve_simple_question']:
    is_coding_question = state.get('is_coding_question')
    
    if is_coding_question:
        return 'solve_coding_question'

    else:
        return 'solve_simple_question'

@observe()
def solve_coding_question(state: State):
    user_message = state.get("user_message")

    # OpenAi call
    state["ai_message"] = "Here is your coding answer"
    return state
@observe()
def solve_simple_question(state: State):
    user_message = state.get("user_message")

    # OpenAi call
    state["ai_message"] = "Here is your simple answer"
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("detect_user_query", detect_user_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question", solve_simple_question)
graph_builder.add_node("route", route)

graph_builder.add_edge(START, 'detect_user_query')
graph_builder.add_conditional_edges('detect_user_query', route)
graph_builder.add_edge('solve_coding_question', END)
graph_builder.add_edge('solve_simple_question', END)

graph = graph_builder.compile()


# use call graph

def call_graph():
    state = {
        "user_message": "Hey there! How are you?",
        "ai_message": "",
        "is_coding_question": False
    }

    result = graph.invoke(state)


    print("Final Result: ", result)

call_graph()