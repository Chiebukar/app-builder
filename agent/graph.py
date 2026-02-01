# import external modules
import json
from urllib import response
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.constants import END
from langgraph.graph import StateGraph

# import local modules
from prompts import planner_prompt, architect_prompt
from states import Plan, TaskPlan

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

user_prompt = "Create a simple calculator web application"

def planner_agent(state: dict) -> dict:
    user_prompt = state.get("user_prompt")
    plan = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    if plan is None:
        raise ValueError("Planner Failed to generate a plan.")
    return {"plan": plan}

def architect_agent(state: dict) -> dict:
    plan: Plan = state.get("plan")
    tasks = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))
    if tasks is None:
        raise ValueError("Architect Failed to generate a task plan.")
    task_plan = {"plan": plan, "tasks": tasks.tasks}
    return {"task_plan": task_plan}  


graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_edge(start_key="planner", end_key="architect")
graph.set_entry_point("planner")

agent = graph.compile()
result = agent.invoke({"user_prompt": user_prompt})
print(result)


# Helper to convert Pydantic models (and nested containers) into
# JSON-serializable Python builtins using pydantic v2's `model_dump()`.
def make_serializable(obj):

    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_serializable(v) for v in obj]
    # fallback for builtins (str, int, float, bool, None)
    return obj


# write result to a json file (convert Pydantic models first)
serializable_result = make_serializable(result)
with open('result__.json', 'w') as fp:
    json.dump(serializable_result, fp, indent=4)
