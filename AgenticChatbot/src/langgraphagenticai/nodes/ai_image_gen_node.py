from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.langgraphagenticai.state.state import State
from typing_extensions import TypedDict,Annotated
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
import requests

class AIImageNode:
    def __init__(self,llm,image_client=None):
        """
        Initialize the AIImageNode with API keys for Tavily and OpenAI.
        """
        
        self.llm = llm
        self.state = {}
        self.image_client=image_client

    def enhance_prompt(self, state: dict)  -> dict:
        """
        Enhance the prompt for generating the ai image.
        
        Args:
            prompt (str): User provided prompt string for generating the image
        
        Returns:
            str: Enhanced prompt for generating images
        """
        print("Inside enhance_prompt")
        prompt_template = ChatPromptTemplate.from_messages([
            "system","""Enhance following prompt for generating real world natural image taken by camera, fully realistic. 
            Prompt : {prompt}"""
        ])
        prompt = state["messages"][0]
        model_with_output=self.llm.with_structured_output(Prompt)
        response = model_with_output.invoke(prompt_template.format(prompt=prompt))
        # model_with_output.invoke(prompt)
        print(response)
        self.state['prompt']=response["prompt"]
        state['prompt']=response["prompt"]
        return self.state

    def generate_image(self, state:dict) -> dict:
        """
        Generate image from the given prompt
        
        Args:
            prompt (str): The state dictionary containing 'news_data'.
        
        Returns:
            image path: return the remote path of generated image.
        """
        print("Inside generate_image")
        print(state)
        
        
        prompt_prefix = "photorealistic, candid portrait of a given description with natural skin texture and slight imperfections, standing in a [setting]. Soft natural lighting, shot on 85mm lens, f/1.8, shallow depth of field, creamy background bokeh, 8k resolution, documentary photography style, Description : "
        # dalle_tool = DallEAPIWrapper(model="dall-e-3",size="1792x1024") # Specify dall-e-3
        # image_url = dalle_tool.run(prompt_prefix+state['prompt'])
        image_url = self.image_client.run(prompt_prefix+self.state['prompt'])

        print(image_url)
        state["image_url"] = image_url
        self.state["image_url"] = image_url
        return self.state
    
    def save_image(self, state:dict) -> dict:
        """ Save the image to local directory
        Args:
            image_url (str): The remote url from where image needs to be downloaded and saved.
        
        Returns:
            image dir (str): image needs to be saved in local directory

        """
        print("Inside save_image")
        filename = f"./AIImages/ai_image_1.jpg"
        response = requests.get(self.state['image_url'])
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
                print(f"Image saved successfully as {filename}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
        state['filename']=filename
        self.state['filename']=filename
        return self.state


class Prompt(TypedDict):
    """Enhanced and optimized Prompt details"""
    prompt:Annotated[str,...,"Enhanced prompt details"]
