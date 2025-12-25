import json

from src.preprocessing.question_understanding import QuestionUnderstanding
from src.retrieval.retriever import Retriever
from src.generation.generator import Generator, ImageDescriptionGenerator
from src.preprocessing.pixtral_parser import parse_pixtral_json_simple

class TravelRAG:
    def __init__(self):
        print("🔧 Initializing TravelRAG pipeline...")
        self.question_understanding = QuestionUnderstanding()
        self.retriever = Retriever()
        self.generator = Generator()
        self.image_describer = ImageDescriptionGenerator()

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


    def answer_image(self, pic_b64: str, caption: str = "") -> str:
        """
        Full image → RAG pipeline:
        image → pixtral → structured text → retrieval → answer
        """

        image_description_raw = self.image_describer.generate_answer(pic_b64)
        try:
            image_description = parse_pixtral_json_simple(image_description_raw)
        except ValueError:
            # если Pixtral сломался
            image_description = {
                "name": "Unknown",
                "location": "Unknown",
                "setting": "Unknown"
            }
        # Build text query for RAG
        image_query_parts = []
        if image_description["name"] != "Unknown":
            image_query_parts.append(
                f"This place is {image_description['name']}."
            )
        if image_description["location"] != "Unknown":
            image_query_parts.append(
                f"It is located in {image_description['location']}."
            )
        if image_description["setting"] != "Unknown":
            image_query_parts.append(
                f"The setting is {image_description['setting']}."
            )
        image_query = " ".join(image_query_parts)
        # Merge with user caption (if any)
        if caption.strip():
            final_query = f"{image_query}\n\nUser question:\n{caption}"
        else:
            final_query = image_query
        return self.answer(final_query)