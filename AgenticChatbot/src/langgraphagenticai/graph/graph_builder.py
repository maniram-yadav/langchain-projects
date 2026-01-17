from langgraph.graph import StateGraph, START,END, MessagesState
from langgraph.prebuilt import tools_condition,ToolNode
from langchain_core.prompts import ChatPromptTemplate
from src.langgraphagenticai.state.state import State

from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools,create_tool_node

from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode
from src.langgraphagenticai.nodes.politics_news_node import PoliticsNewsNode
from src.langgraphagenticai.nodes.ai_image_gen_node import AIImageNode




class GraphBuilder:

    def __init__(self,model,image_client=None):
        self.llm=model
        self.graph_builder=StateGraph(State)
        self.image_client=image_client

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """
        self.basic_chatbot_node=BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot with tool 
        capabilities, and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """
        # Define the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # Define llm
        llm = self.llm

        # Define teh chatbot node
        
        # Define chatbot node
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

        # Add nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        # Define conditional and direct edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools","chatbot")


    def ai_news_build_graph(self):
        # Initialize the AINewsNode
        ai_news_node = AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)


    def politics_news_build_graph(self):
        # Initialize the PoliticsNewsNode
        politics_news_node = PoliticsNewsNode(self.llm)

        self.graph_builder.add_node("fetch_news", politics_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", politics_news_node.summarize_news)
        self.graph_builder.add_node("save_result", politics_news_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)

    def generate_image_build_graph(self):
       
        # Initialize the AIImageNode
        aiimage_news_node = AIImageNode(self.llm,self.image_client)

        self.graph_builder.add_node("enhance_prompt", aiimage_news_node.enhance_prompt)
        self.graph_builder.add_node("generate_image", aiimage_news_node.generate_image)
        self.graph_builder.add_node("save_image", aiimage_news_node.save_image)

        self.graph_builder.set_entry_point("enhance_prompt")
        self.graph_builder.add_edge("enhance_prompt", "generate_image")
        self.graph_builder.add_edge("generate_image", "save_image")
        self.graph_builder.add_edge("save_image", END)



    def setup_graph(self,usecase : str):
        """
        Sets up the graph for the seletcted use case.
        """
        if usecase=="Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase=="Chatbot with Tool":
            self.chatbot_with_tools_build_graph()
        if usecase=="AI News":
            self.ai_news_build_graph()
        if usecase=="Politics News":
            self.politics_news_build_graph()
        if usecase=="Image Generation":
            self.generate_image_build_graph()

        graph = self.graph_builder.compile()
        return graph
