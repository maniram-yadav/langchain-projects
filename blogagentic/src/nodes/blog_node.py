from src.states.blog_state import BlogState,Blog
from langchain.messages import HumanMessage
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
        print(" =========>  Inside content_generation")
        print(state)
        if "topic" in state and state["topic"]:
            system_prompt = """You are exprt blog writer. Use Markdown formatting.
                Generate a 50 word blog content with detailed breakdown for the {topic}
               """
            system_message = system_prompt.format(topic=state["topic"])
            llm_with_output = self.llm.with_structured_output(Content)
            response = llm_with_output.invoke(system_message)
            print(response)
            # "current_language":state["current_language"],
            return {"blog" : { "title": state['blog']['title'], "content":response['content']}}

    def translation(self,state:BlogState):
        """
        Translate the content in specified langauge
        
        :param self: Description
        :param state: Description
        :type state: BlogState
        """       
        print(" =========> Insie translation")
        translation_prompt = """ 
            Translate the following content into {current_language}.
            - Maintain the original tone, style and formatting.
            - Adapt cultural references and idoms to be appropriate for {current_language}

            ORIGINAL Content : 
            {blog_content}
            """
        print(state)
        blog_content = state["blog"]["content"]
        messages = [
            HumanMessage(translation_prompt.format(current_language=state["current_language"],
                                                   blog_content=blog_content))
        ]
        translation_content = self.llm.with_structured_output(Blog).invoke(messages)
        state["blog"]=translation_content
        print(state)
        return state

    def route(self,state:BlogState):
        print("route ==> ",state)
        return {**state,"current_language":state['current_language']}
    
    def route_decision(self,state:BlogState):
        """ 
        Route the content to the respective translation function
        """
        if state["current_language"]=="hindi":
            return "hindi"
        elif state["current_language"]== "french":
            return "french"
        else :
            return state['current_language']
        


class Title(TypedDict):
    title:str

class Content(TypedDict):
    content:str
