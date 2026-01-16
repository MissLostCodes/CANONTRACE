from agents.base_agent import BaseAgent
from prompts import load_prompt, build_prompt


QUESTION_AGENT_PROMPT = build_prompt(
    load_prompt("agent1_question_generation.txt")
)


class QuestionGenerationAgent:
    def __init__(self, gemini_llm):
        """
        Question generation agent using ChatAgent + init_chat_model
        """
        self.agent = BaseAgent(
            llm=gemini_llm.get_model(),
            system_prompt=QUESTION_AGENT_PROMPT,
        )

    def run(self, character: str, content: str) -> str:
        user_prompt = f"""
Character Name: {character}

Hypothetical Backstory:
{content}
"""

        return self.agent.invoke(user_prompt)
