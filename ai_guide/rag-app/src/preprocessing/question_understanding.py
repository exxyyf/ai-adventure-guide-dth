import sys
import os
from typing import Optional, Dict
import json
from dotenv import load_dotenv

from mistralai import Mistral

# load_dotenv()

if not os.getenv("MISTRAL_API_KEY"):
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))


class QuestionUnderstanding:
    def __init__(self, model_name: str = "mistral-small-latest"):
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model_name = model_name

    def analyze(self, query: str) -> Dict:
        """Проводит LLM-анализ пользовательского запроса и возвращает структуру."""

        system_prompt = """
You are a specialized travel query analyzer. Your task is to parse user messages and extract structured information for a travel assistance system.

OUTPUT REQUIREMENT: Return ONLY valid JSON. No markdown, no explanations, no additional text.

JSON SCHEMA:
{
  "intent": "string - see intent types below",
  "entities": {
    "locations": ["cities, countries, regions, landmarks"],
    "activities": ["mentioned activities or interests"]
  },
  "clarified_query": "string - optimized version for semantic search",
  "needs_more_info": boolean
}

INTENT TYPES:
- "information" - seeking facts about destinations, culture, weather, costs
- "recommendation" - asking for suggestions, best places, what to do/see
- "navigation" - directions, routes, how to get somewhere
- "visa" - visa requirements, documentation, entry rules
- "safety" - security concerns, travel warnings, health precautions
- "transport" - flights, trains, buses, car rental, schedules
- "accommodation" - hotels, hostels, booking, where to stay
- "dining" - restaurants, local food, where to eat
- "budget" - cost planning, price estimates, affordability
- "unknown" - unclear or off-topic query

EXTRACTION RULES:

1. ENTITIES:
   - Extract ALL geographic mentions (cities, countries, regions, landmarks)
   - Normalize location names to standard forms (e.g., "NYC" → "New York City")
   - Include implicit locations from context (e.g., "there" if previous location known)
   - Identify activities: "hiking", "museums", "beaches", "nightlife"

2. CLARIFIED_QUERY:
   - Expand abbreviations and slang
   - Make implicit context explicit
   - Add relevant keywords for better retrieval
   - Keep natural language structure
   - Example: "cheap eats paris" → "affordable restaurants and local food in Paris France"

3. NEEDS_MORE_INFO:
   Set to TRUE when:
   - No clear intent can be determined
   - Critical details missing (e.g., no location for location-specific query)
   - Query is too vague ("tell me about travel")
   - Ambiguous references ("what about there?", "is it safe?")
   
   Set to FALSE when:
   - Query is complete enough to retrieve relevant information
   - Intent and key entities are clear

4. SPECIAL CASES:
   - Multi-destination queries: list all locations in entities
   - Comparative queries: extract all compared entities
   - Follow-up queries: mark needs_more_info=true if context is required
   - Off-topic: intent="unknown", explain nothing in JSON

EXAMPLES:

Input: "best time to visit japan"
Output:
{
  "intent": "information",
  "entities": {"locations": ["Japan"], "activities": []},
  "clarified_query": "best time of year and season to visit Japan",
  "needs_more_info": false
}

Input: "cheap eats?"
Output:
{
  "intent": "recommendation",
  "entities": {"locations": [], "activities": ["dining"]},
  "clarified_query": "affordable restaurants and inexpensive food options",
  "needs_more_info": true,
}

CRITICAL: Output ONLY the JSON object. No preamble, no markdown formatting, no explanations.
"""
        user_prompt = f"User query: {query}\nReturn JSON:"

        response = self.client.chat.complete(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )

        data = response.choices[0].message.content

        # Обработка ошибок: иногда модель может добавить текст до/после JSON
        json_str = self._extract_json(data)
        return json.loads(json_str)

    @staticmethod
    def _extract_json(text: str) -> str:
        """Извлекает JSON из текста (на случай, если модель добавит лишнее)."""
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("No JSON found in LLM output")
        return text[start : end + 1]


if __name__ == "__main__":
    # Проверяем, что аргумент передан
    if len(sys.argv) < 2:
        print('Usage: python question_understanding.py "your question here"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    q = QuestionUnderstanding()

    try:
        result = q.analyze(query)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
