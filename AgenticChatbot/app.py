from src.langgraphagenticai.main import load_langgraph_agenticai_app
# from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.ui.uiconfigfile import Config
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

# dalle_tool = DallEAPIWrapper(model="dall-e-3",size="1792x1024") # Specify dall-e-3
# image_url = dalle_tool.run(detailed_prompt)

if __name__=="__main__":
    load_langgraph_agenticai_app()


# if __name__=="__main__":
    # config = Config()
    # print(config)
    # print(config.get_page_title())
    # print(config.get_llm_options())
    # streamlitui = LoadStreamlitUI()