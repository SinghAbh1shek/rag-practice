from typing import Annotated
from typing_extensions import TypedDict
import os
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool()
def run_command(cmd: str):
    """
    Takes the command line prompt and executes it on the user's machine and return the output of the command.
    
    Example: run_command(cmd="dir") where dir is command to list the files.
    """
    result = os.system(command=cmd)
    return result

@tool
def write_file(file_path: str, content: str) -> str:
    """Write to a file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            return f"File {file_path} written successfully"
    except Exception as e:
        return f"Error writing file: {e}"

llm = init_chat_model(
    model_provider="google_genai", model="gemini-1.5-flash"
)

llm_with_tool = llm.bind_tools(tools=[run_command, write_file])

def Chatbot(state: State):
    system_prompt = SystemMessage(content="""
    You are an helpful AI coding assistant who takes input as input from user and based on the available tools you choose the correct tool and execute the commands.

    You can even execute commands and help user with the output of the command.

    You have deep expertise in:
    You are highly skilled in:
    - Frontend: React (Vite preferred), Vue, Angular, HTML, CSS, Tailwind, JavaScript, TypeScript
    - Backend: Node.js (Express), Python (Django, Flask), Java (Spring Boot), Ruby on Rails
    - Databases: PostgreSQL, MySQL, SQLite, MongoDB, Firebase
    - DevOps: Docker, Git, CI/CD, GitHub Actions, AWS deployment
    - Tooling: npm, pip, Docker CLI, terminal commands

    TOOLING INSTRUCTION
    You can interact with the environment via the following tools:
    
     `run_command(command: str)`  
        - Executes a shell command (string input only).
        - Do NOT pass dictionaries or malformed commands.
        - Windows OS assumed — use correct syntax accordingly.

    `write_file(file_path: str, content: str)`  
        - Writes the given content to the specified path.
        - Ensure that content is complete and context-aware.


    call the relavant tools
    """
)
    message = llm_with_tool.invoke([system_prompt] + state["messages"])
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}

tool_node = ToolNode(tools=[run_command, write_file])

graph_builder = StateGraph(State)

graph_builder.add_node("Chatbot", Chatbot)
graph_builder.add_node("tools", tool_node)


graph_builder.add_edge(START, 'Chatbot')
graph_builder.add_conditional_edges("Chatbot", tools_condition)

graph_builder.add_edge('tools', "Chatbot")
graph_builder.add_edge('Chatbot', END)


graph = graph_builder.compile()

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)