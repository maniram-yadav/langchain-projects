from src.states.blog_state import BlogState
from typing import TypedDict

class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self,llm):
        self.llm = llm

    def title_creation(self,state:BlogState):

        """ 
        create the title for the blog
        """
        if "topic" in state and state["topic"]:
            prompt = """
                    You are an expert blog content writer. Use Markdown formatting. 
                    Generate a blog title for the {topic}. The Title should be creative and SEO friendly

                 """
            
            system_message = prompt.format(topic=state["topic"])
            llm_with_output = self.llm.with_structured_output(Title)
            response = llm_with_output.invoke(system_message)
            print(response)
            return {"blog":{"title":response['title']}}
        
    def content_generation(self,state:BlogState):

        if "topic" in state and state["topic"]:
            system_prompt = """You are exprt blog writer. Use Markdown formatting.
                Generate a detailed blog content with detailed breakdown for the {topic}
               """
            system_message = system_prompt.format(topic=state["topic"])
            llm_with_output = self.llm.with_structured_output(Content)
            response = llm_with_output.invoke(system_message)
            print(response)
            return {"blog" : {"title": state['blog']['title'], "content":response['content']}}
        
class Title(TypedDict):
    title:str

class Content(TypedDict):
    content:str