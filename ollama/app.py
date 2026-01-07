import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

#langsmith tracing
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2']='true'
os.environ['LANGCHAIN_PROJECT']="Simple Chat App"

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respons to the question asked"),
        ("user","Question:{question}")
    ]
)

## streamlit framework
st.title("Langchain Demo with Open AI")
input_text=st.text_input("What question you have in your mind ?")


## open ai llm model
llm = ChatOpenAI(model="gpt-4o")
output_parser=StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question":input_text}))
