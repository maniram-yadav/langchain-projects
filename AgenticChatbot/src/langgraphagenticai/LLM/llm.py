from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from .groqllm import GroqLLM
from .openai import OpenAILLM

def get_AI_Model(user_control_input):
        llm = None
        if user_control_input["selected_llm"] == 'Groq':
            llm = GroqLLM(user_control_input)
            # groq_api_key = user_control_input["GROQ_API_KEY"]
            # selected_groq_model = user_control_input["selected_groq_model"]
            # llm = ChatGroq(api_key=groq_api_key,model=selected_groq_model)
        elif user_control_input["selected_llm"] == 'OpenAI':
            llm = OpenAILLM(user_control_input)
            # groq_api_key = user_control_input["GROQ_API_KEY"]
            # selected_groq_model = user_control_input["selected_groq_model"]
            # llm = ChatOpenAI(api_key=groq_api_key,model=selected_groq_model)
        return llm



