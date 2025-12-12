import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()


class Generator:
    def __init__(self, model_name: str = "mistral-small-latest"):
        self.model_name = model_name
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    def generate_answer(self, question: str, retrieved_chunks: list, max_tokens: int = 300) -> str:
        """
        Generate a text answer using Mistral LLM based on retrieved context chunks.

        :param question: clarified user question
        :param retrieved_chunks: list of text chunks retrieved from FAISS
        :param max_tokens: maximum length of the generated answer
        """

        system_prompt = """
You are an expert travel assistant. 
Provide a clear, well-structured, accurate answer using ONLY the context provided.
Do NOT invent facts. If context is insufficient, say this directly.
        """

        user_prompt = f"""
Context:
{retrieved_chunks}

Question:
{question}

Write a complete helpful answer:
        """

        try:
            response = self.client.chat.complete(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.3,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Generator error: {str(e)}"
