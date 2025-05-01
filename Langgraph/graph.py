from langfuse import Langfuse
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
from dotenv import load_dotenv
from langfuse.decorators import observe
from langfuse.openai import openai
import os
from pydantic import BaseModel

load_dotenv()
GOOGLE_API_KEY = os.getenv("Gemini_API")

client = openai.Client(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


# Schema
class DetectCallResponse(BaseModel):
    is_coding_question: bool

class aiMessages(BaseModel):
    ai_message: str

class State(TypedDict):
    user_message: str
    ai_message: str
    is_coding_question: bool

@observe()
def detect_user_query(state: State):
    user_message = state.get("user_message")

    # OpenAi call

    SYSTEM_PROMPT = """
    You are an helpful AI assistant. Your job is to detect if the user's query is related to coding or not.

    Return the response in specified JSON boolean only.
    """

    result = client.beta.chat.completions.parse(
        model="gemini-1.5-flash",
        response_format=DetectCallResponse,
        messages=[
            {'role':'system', 'content':SYSTEM_PROMPT},
            {'role':'user', 'content':user_message},
        ]
    )
    # print(result.choices[0].message.parsed)

    state["is_coding_question"] = result.choices[0].message.parsed.is_coding_question
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
    SYSTEM_PROMPT = """
    You are an helpful AI assistant who is specialized in coding. Your job is give the best answer according to the user query.

    Return the response in specified string only.
    """
    result = client.beta.chat.completions.parse(
        model="gemini-1.5-flash",
        response_format=aiMessages,
        messages=[
            {'role':'system', 'content':SYSTEM_PROMPT},
            {'role':'user', 'content':user_message},
        ]
    )
    # print(result.choices[0].message.parsed)


    state["ai_message"] = result.choices[0].message.parsed.ai_message
    return state
@observe()
def solve_simple_question(state: State):
    user_message = state.get("user_message")

    # OpenAi call
    SYSTEM_PROMPT = """
    You are an helpful AI assistant who is specialized in chatting. Your job is to act like chatbot.

    Return the response in specified string only.
    """
    result = client.beta.chat.completions.parse(
        model="gemini-1.5-flash",
        response_format=aiMessages,
        messages=[
            {'role':'system', 'content':SYSTEM_PROMPT},
            {'role':'user', 'content':user_message},
        ]
    )
    # print(result.choices[0].message.parsed)


    state["ai_message"] = result.choices[0].message.parsed.ai_message
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
    query = input('>>> ')
    state = {
        "user_message": query,
        "ai_message": "",
        "is_coding_question": False
    }

    result = graph.invoke(state)


    print("Final Result: ", result)
    # print("Final Result: ", result.get('ai_message'))
while True:
    call_graph()
    exitBtn = input("press exit to exit and enter to continue: ")
    if exitBtn == 'exit':
        print("Exiting...")
        break