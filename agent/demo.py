from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

class Schema(BaseModel):
    price: float = Field(description="The current price of the stock")
    eps: float = Field(description="The earnings per share of the company")


resp = llm.with_structured_output(Schema).invoke("Extract Price and EPS from this report: Nvidia reported quarterly revenue of $7.19 billion, up 101% year over year," \
" driven by strong demand for its AI and gaming products. The company's earnings per share (EPS) came in at $1.36," \
" and their current price is $400. " \
" The robust financial performance highlights Nvidia's dominant position in the semiconductor industry and its successful expansion " \
"into new markets such as AI and data centers.")
print(resp)