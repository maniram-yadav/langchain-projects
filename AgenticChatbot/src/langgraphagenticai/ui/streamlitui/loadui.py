import streamlit as st
import os
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls={}

    
    def initialize_session(self):
        return {
        "current_step": "requirements",
        "requirements": "",
        "user_stories": "",
        "po_feedback": "",
        "generated_code": "",
        "review_feedback": "",
        "decision": None
    }
  

    def load_streamlit_ui(self):
        
        st.set_page_config(page_title=self.config.get_page_title(),layout="wide")
        st.header(self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
        st.session_state.IsSDLC = False

        with st.sidebar:
            # Get options from config
            
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selections
            self.user_controls["selected_llm"] = st.selectbox("Select LLM",llm_options)

            if self.user_controls["selected_llm"] == 'Groq' or self.user_controls["selected_llm"] == 'OpenAI':
                #Model selection
                model_options=self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Model",model_options)
                self.user_controls["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("API Key",type="password")

                #validate api key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your API Key to proceed. Don't have ?")
            
            # Usecase selection
            self.user_controls["selected_usecase"]=st.selectbox("Select Usecases",usecase_options)

            if self.user_controls["selected_usecase"]=="Chatbot with Tool" or self.user_controls["selected_usecase"] =="AI News" or  self.user_controls["selected_usecase"] == "Politics News":

                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API KEY",
                                                                                        type="password")
                # Validate API key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY_API_KEY key to proceed. Don't have? refer : https://app.tavily.com/home")
                
                elif self.user_controls['selected_usecase']=="AI News":
                    st.subheader("AI News Explorer")

                    with st.sidebar:
                        time_frame = st.selectbox("📅 Select Time Frame",
                            ["Daily", "Weekly", "Monthly"],
                            index=0)
                    
                    if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                        st.session_state.IsFetchButtonClicked = True
                        st.session_state.timeframe = time_frame
                    else :
                        st.session_state.IsFetchButtonClicked = False
                elif self.user_controls['selected_usecase']=="Politics News":
                    st.subheader("Politics News Explorer")

                    with st.sidebar:
                        time_frame = st.selectbox("📅 Select Time Frame",
                            ["Daily", "Weekly", "Monthly"],
                            index=0)
                    
                    if st.button("🔍 Fetch Latest Politics News", use_container_width=True):
                        st.session_state.IsFetchButtonClicked = True
                        st.session_state.timeframe = time_frame
                    else :
                        st.session_state.IsFetchButtonClicked = False
                if "state" not in st.session_state:
                    st.session_state.state = self.initialize_session()
            
        return self.user_controls


if __name__=="__main__":
    ui = LoadStreamlitUI()
    print(ui)

