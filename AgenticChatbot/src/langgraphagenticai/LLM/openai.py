import os
import streamlit as st
from langchain_openai import ChatOpenAI
from .llm_model import  LLMModel
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

class OpenAILLM(LLMModel):
    def __init__(self,user_control_input):
        self.user_control_input = user_control_input

    def get_llm_model(self):
        try:
            groq_api_key = self.user_control_input["GROQ_API_KEY"]
            selected_groq_model = self.user_control_input["selected_groq_model"]
            if groq_api_key=='' and os.environ["GROQ_API_KEY"]=='':
                st.error("Please enter teh Groq API Key")
            llm = ChatOpenAI(api_key=groq_api_key,model=selected_groq_model)

        except Exception as e:
            raise ValueError(f"Error occured with Exception :  {e}")
        return llm
    
    def get_image_model(self):
        image_client=None
        try:
            groq_api_key = self.user_control_input["GROQ_API_KEY"]
            selected_groq_model = self.user_control_input["selected_groq_model"]
            if groq_api_key=='' and os.environ["GROQ_API_KEY"]=='':
                st.error("Please enter teh Groq API Key")
            
            image_client = DallEAPIWrapper(api_key=groq_api_key,model="dall-e-3",size="1792x1024") # Specify dall-e-3


        except Exception as e:
            raise ValueError(f"Error occured with Exception :  {e}")
        return image_client
    
    
