from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from prompts import planner_prompt
from states import Plan

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

user_prompt = "Create a simple calculator web application"

 


resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
print(resp)