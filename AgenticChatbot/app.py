from src.langgraphagenticai.main import load_langgraph_agenticai_app
# from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.ui.uiconfigfile import Config

if __name__=="__main__":
    load_langgraph_agenticai_app()


# if __name__=="__main__":
    # config = Config()
    # print(config)
    # print(config.get_page_title())
    # print(config.get_llm_options())
    # streamlitui = LoadStreamlitUI()