from typing import Dict, Any
from langchain.messages import SystemMessage, HumanMessage


class BaseAgent:
    """
    Simple chat agent built on top of an init_chat_model LLM.
    """

    def __init__(self, llm, system_prompt: str):
        self.llm = llm
        self.system_prompt = system_prompt

    def invoke(self, user_prompt: str | Dict[str, Any]) -> str:
        """
        Accepts either:
        - a raw string
        - or a dict to be formatted beforehand
        """
        print("---------Base agent invoked------------")
        if isinstance(user_prompt, dict):
            user_prompt = user_prompt["prompt"]

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_prompt),
        ]

        response = self.llm.invoke(messages)


        if hasattr(response, "content"):
            if isinstance(response.content, list):
                return response.content[0].get("text", "")
            return response.content



        return str(response)
