import streamlit as st
import os
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        # print("Hello UI")
        self.config = Config()
        
        print(self.config)
        print(self.config.get_page_title())
        self.user_controls={}

    def load_streamlit_ui(self):
        print(self.config)
        st.set_page_config(page_title=self.config.get_page_title(),layout="wide")
        st.header(""+self.config.get_page_title())

        with st.sidebar:
            # Get options from config
            
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selections
            self.user_controls["selected_llm"] = st.selectbox("Selcct LLM",llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                #Model selection
                model_options=self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Model",model_options)
                self.user_controls["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("API Key",type="password")

                #validate api key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your API Key to proceed. Don't have ?")
            
            # Usecase selection
            self.user_controls["selected_usecase"]=st.selectbox("Select Usecases",usecase_options)

            if self.user_controls["selected_usecase"]=="Chatbot with Tool":
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API KEY",
                                                                                        type="password")
                            # Validate API key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY_API_KEY key to proceed. Don't have? refer : https://app.tavily.com/home")

        return self.user_controls


if __name__=="__main__":
    ui = LoadStreamlitUI()
    print(ui)

