# import external modules
import json
from urllib import response
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain.globals import set_verbose, set_debug
from langchain.agents import create_react_agent

# import local modules
from .prompts import planner_prompt, architect_prompt, coder_sys_prompt
from .states import Plan, TaskPlan
from .tools import get_current_directory, write_file, read_file, list_files, run_cmd, init_project_root

load_dotenv() # Load environment variables from .env file

set_debug(True)
set_verbose(True)

llm = ChatGroq(model="openai/gpt-oss-120b") # Initialize the LLM

# Define the planner agent
def planner_agent(state: dict) -> dict:
    user_prompt = state.get("user_prompt")
    plan = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    if plan is None:
        raise ValueError("Planner Failed to generate a plan.")
    return {"plan": plan}

# Define the architect agent
def architect_agent(state: dict) -> dict:
    plan: Plan = state.get("plan")
    tasks = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))
    if tasks is None:
        raise ValueError("Architect Failed to generate a task plan.")
    task_plan = {"plan": plan, "tasks": tasks.tasks}
    return {"task_plan": task_plan}  

# Define the coder agent
def coder_agent(state: dict) -> dict:
    tasks: list = state.get("task_plan").get("tasks")
    current_task_idx = 0
    current_task = tasks[current_task_idx]

    existing_content = read_file(current_task.filepath)

    user_prompt = (
        f"Task: {current_task.description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )
    system_prompt = coder_sys_prompt()
    coder_tools = [write_file, read_file, list_files, get_current_directory]
    react_agent = create_react_agent(llm, coder_tools)
    response = react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})


    # return {"code": response.content}  

    

# Build the state graph
graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_edge(start_key="planner", end_key="architect")
graph.add_edge(start_key="architect", end_key="coder")
graph.set_entry_point("planner")
agent = graph.compile()


# convert Pydantic models to JSON format.
def make_serializable(obj):

    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_serializable(v) for v in obj]
    # fallback for builtins (str, int, float, bool, None)
    return obj


if __name__ == "__main__":
    # Run the agent with a user prompt
    user_prompt = "Create a simple calculator web application"
    result = agent.invoke({"user_prompt": user_prompt})
    print(result)

    # Save the result to a JSON file
    serializable_result = make_serializable(result)
    with open("result.json", "w") as f:
        json.dump(serializable_result, f, indent=4)