import argparse
import os
import sys

# Импорты модулей
from src.preprocessing.question_understanding import QuestionUnderstanding
from src.retrieval.retriever import Retriever
from src.generation.generator import Generator



def main():
    parser = argparse.ArgumentParser(description="AI Travel Assistant RAG Service")
    parser.add_argument("--q", "--query", type=str, required=True, help="User question")
    args = parser.parse_args()

    user_query = args.q

    # -------- 1. Анализ запроса --------
    print("\n🔍 Understanding query...")
    try:
        question_understanding = QuestionUnderstanding()
        analysis = question_understanding.analyze(user_query)
    except Exception as e:
        print(f"Error in QuestionUnderstanding: {e}")
        sys.exit(1)

    print("➡ Intent:", analysis.get("intent"))
    print("➡ Entities:", analysis.get("entities"))
    print("➡ Clarified query:", analysis.get("clarified_query"))
    print("➡ Needs more info:", analysis.get("needs_more_info"))

    clarified_query = analysis.get("clarified_query", user_query)

    # -------- 2. Retrieval --------
    print("\n📚 Retrieving relevant context...")
    try:
        retriever = Retriever()
        retrieved_chunks = retriever.retrieve(clarified_query)
    except Exception as e:
        print(f"Error in Retriever: {e}")
        sys.exit(1)

    print(f"➡ Retrieved {len(retrieved_chunks)} chunks")

    # -------- 3. Generation --------
    print("\n✍ Generating answer...")
    try:
        generator = Generator()
        answer = generator.generate_answer(clarified_query, retrieved_chunks)
    except Exception as e:
        print(f"Error in Generator: {e}")
        sys.exit(1)

    print("\n💬 Final Answer:")
    print(answer)


if __name__ == "__main__":
    # Запуск из корня проекта:
    # python -m src.main --q "your question here"
    main()
