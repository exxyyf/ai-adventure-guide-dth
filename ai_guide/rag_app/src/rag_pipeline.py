from src.preprocessing.question_understanding import QuestionUnderstanding
from src.retrieval.retriever import Retriever
from src.generation.generator import Generator


class TravelRAG:
    def __init__(self):
        print("🔧 Initializing TravelRAG pipeline...")
        self.question_understanding = QuestionUnderstanding()
        self.retriever = Retriever()
        self.generator = Generator()

    def answer(self, user_query: str) -> str:
        # 1. Understanding
        analysis = self.question_understanding.analyze(user_query)
        clarified_query = analysis.get("clarified_query", user_query)

        # 2. Retrieval
        retrieved_chunks = self.retriever.retrieve(clarified_query)

        # 3. Generation
        answer = self.generator.generate_answer(
            clarified_query,
            retrieved_chunks
        )

        return answer
