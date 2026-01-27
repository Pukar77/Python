import os
import json
import math
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from google import genai


SIMILARITY_THRESHOLD = 0.85

ARTICLES_DIR = Path("articles")
QUIZ_DIR = Path("Quiz")
ERROR_DIR = Path("QuizErrors")

QUIZ_DIR.mkdir(exist_ok=True)
ERROR_DIR.mkdir(exist_ok=True)

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))



class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_answer: str
    confidence_score: float

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    return dot / (norm1 * norm2)

def load_existing_embeddings():
    """Load embeddings from all saved quiz JSON files"""
    embeddings = []

    for file in QUIZ_DIR.glob("*_quiz.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            if "embedding" in data:
                embeddings.append({
                    "question": data["question"],
                    "embedding": data["embedding"],
                    "source_file": file.name
                })
        except Exception:
            continue

    return embeddings


def generate_quiz(markdown_text: str) -> dict:
    prompt = f"""
You are an automated quiz generator.

You will be given the content of EXACTLY ONE article.
From this article, generate EXACTLY ONE multiple-choice question.

Rules:
- The question must be based ONLY on the provided article
- Provide exactly 4 options
- There must be exactly ONE correct answer
- The correct answer must be one of the options
- Provide a confidence_score between 0 and 1
- Do NOT repeat or paraphrase common generic questions

Return ONLY valid JSON.

Required JSON format:
{{
  "question": "",
  "options": ["", "", "", ""],
  "correct_answer": "",
  "confidence_score": 0.0
}}

ARTICLE CONTENT:
----------------
{markdown_text}
"""

    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": QuizQuestion,
            "temperature": 0.1
        }
    )

    if not response.parsed:
        raise ValueError("Quiz generation failed")

    return response.parsed.model_dump()

def generate_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return response.embeddings[0].values



def process_markdown(markdown_path: Path):
    print(f"\n📄 Processing: {markdown_path.name}")

    markdown_text = markdown_path.read_text(encoding="utf-8")

    quiz_data = generate_quiz(markdown_text)
    new_embedding = generate_embedding(quiz_data["question"])

    existing_embeddings = load_existing_embeddings()

    for item in existing_embeddings:
        similarity = cosine_similarity(new_embedding, item["embedding"])

        if similarity >= SIMILARITY_THRESHOLD:
            print(" Duplicate question detected!")
            print(f"   New: {quiz_data['question']}")
            print(f"   Existing: {item['question']}")
            print(f"   Similarity: {similarity:.2f}")

            # Save error JSON instead of quiz
            error_data = {
                "status": "error",
                "reason": "Similar question detected",
                "similarity_score": similarity,
                "new_question": quiz_data["question"],
                "existing_question": item["question"],
                "matched_with": item["source_file"]
            }

            error_file = ERROR_DIR / f"{markdown_path.stem}_error.json"
            error_file.write_text(json.dumps(error_data, indent=2), encoding="utf-8")

            print(f"Error file saved: {error_file.name}")
            return  



    quiz_data["embedding"] = new_embedding

    output_file = QUIZ_DIR / f"{markdown_path.stem}_quiz.json"
    output_file.write_text(json.dumps(quiz_data, indent=2), encoding="utf-8")

    print(f" Quiz saved: {output_file.name}")



#Entry point of the main logic
def main():
    files = sorted(ARTICLES_DIR.glob("article_*.md"))

    if not files:
        print(" No markdown files found")
        return

    for file in files:
        process_markdown(file)

if __name__ == "__main__":
    main()
