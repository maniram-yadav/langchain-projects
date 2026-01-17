from abc import ABC, abstractmethod

class LLMModel(ABC): 
    @abstractmethod
    def get_llm_model(self):
        pass
