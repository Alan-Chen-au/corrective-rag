from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

llm = ChatOpenAI(temperature=0).bind()
prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()
# generation_chain = prompt | llm | (lambda msg: msg.content)
intermediate_chain = prompt | llm
