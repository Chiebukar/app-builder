# import external modules
import json
from urllib import response
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain_core.globals import set_verbose, set_debug
from langgraph.prebuilt import create_react_agent

# import local modules
from .prompts import planner_prompt, architect_prompt, coder_sys_prompt
from .states import Plan, TaskPlan, CoderState
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
    coder_state: CoderState = state.get("coder_state")

    if coder_state is None:
        # First time the coder agent is invoked, initialize the coder state
        task_plan: TaskPlan = state.get("task_plan")
        coder_state: CoderState = {
            "task_plan": task_plan,
            "current_step_idx": 0,
        }

    steps = coder_state.get("tasks")
    if coder_state.get("current_step_idx") >= len(steps):
        return {"code_state": coder_state, "Status": "Done"}
    
    current_task = steps[coder_state.get("current_step_idx")]
    existing_content= read_file(current_task.filepath)

    system_prompt = coder_sys_prompt()
    user_prompt = (
        f"Task: {current_task.description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    
    coder_tools = [write_file, read_file, list_files, get_current_directory]
    react_agent = create_react_agent(llm, coder_tools)
    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})


    # Update the coder state to reflect the completion of the current task
    coder_state["current_step_idx"] += 1
    return {"code_state": coder_state}  

    

# Build the state graph
graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

# Define the edges between the nodes to specify the flow of information
graph.add_edge(start_key="planner", end_key="architect")
graph.add_edge(start_key="architect", end_key="coder")

# Add a conditional edge from the coder node to itself to allow for multiple iterations
#  until all tasks are completed
graph.add_conditional_edges(
    "coder",
    lambda state: "end" if state.get("Status") == "Done" else "coder",
    {"end": END, "coder": "coder"}
)

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
    user_prompt = "Create a colurful calculator web application using React for the frontend and Node.js for the backend and a responsive design."
    result = agent.invoke({"user_prompt": user_prompt}, 
                          {"recursion_limit": 100})
    # print(result)

    # # Save the result to a JSON file
    # serializable_result = make_serializable(result)
    # with open("result.json", "w") as f:
    #     json.dump(serializable_result, f, indent=4)