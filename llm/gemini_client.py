from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiLLM:
    def __init__(
        self,
        model_name="gemini-2.5-flash",
        api_key="",
        temperature=0.5,
        timeout=10,
        max_tokens=2048,
    ):
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            api_key=api_key,
            temperature=temperature,
            timeout=timeout,
            max_tokens=max_tokens,
            response_format="json"
        )

    def get_model(self):
        return self.model
