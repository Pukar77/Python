from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os, json, re
from typing import Any

load_dotenv()

router = APIRouter(tags=["API For Summary Generation"])
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class user_input(BaseModel):
    ai_format: str
    resume_rendered: list[dict[str, Any]]


def get_format_instruction(ai_format: str) -> str:
    format_map = {
        "ai 1st person":      "Write the summary in first person (e.g., 'I am a software developer...').",
        "ai 3rd person":      "Write the summary in third person (e.g., 'He/She is a software developer...').",
        "ai Anonymize":       "Do not include the candidate's name or any personally identifiable information.",
        "ai Bold Subheading": "Include 2-3 bold subheadings inside the summary to highlight key areas like Skills, Experience, or Expertise.",
        "ai Concise":         "Keep the summary very concise (3-4 sentences maximum) while preserving key information.",
        "ai Education Overview": "Focus more on educational background, academic achievements, and learning journey.",
        "ai Expand":          "Write a more detailed and expanded summary (8-10 sentences) with deeper insights into experience and impact."
    }
    return format_map.get(ai_format, "Follow a standard professional summary format.")


def generate_prompt(data: user_input) -> str:
    resume = data.resume_rendered[0]
    format_instruction = get_format_instruction(data.ai_format)
    return f"""
You are an expert resume writer and career branding specialist.

Your task is to generate a concise, professional summary based on the candidate's resume data.

-------------------------
INPUT
-------------------------
{resume}

-------------------------
FORMAT REQUIREMENT
-------------------------
{format_instruction}

-------------------------
INSTRUCTIONS
-------------------------
1. Analyze: Skills, Experience, Projects, Education, Achievements.
2. Write 5-8 sentences. Formal tone. Highlight strengths and impact.
3. Do NOT use bullet points, headings, or mention "resume".
4. Do NOT include information not present in the input.
5. Output must flow naturally and be grammatically correct.

-------------------------
OUTPUT
-------------------------
Return ONLY the plain summary text. No JSON, no code fences, no labels.
"""


# ── Pricing constants (gpt-4o as of 2025) ─────────────────────────
INPUT_PRICE_PER_TOKEN  = 2.5  / 1_000_000   # $2.50 / 1M tokens
OUTPUT_PRICE_PER_TOKEN = 10.0 / 1_000_000   # $10.00 / 1M tokens


def compute_price(input_tokens: int, output_tokens: int) -> float:
    return round(
        input_tokens  * INPUT_PRICE_PER_TOKEN +
        output_tokens * OUTPUT_PRICE_PER_TOKEN,
        8
    )


# ── SSE helper ────────────────────────────────────────────────────
def sse(event: str, data: dict) -> str:
    """Format a single SSE frame."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# ── Core async generator ──────────────────────────────────────────
async def stream_summary(data: user_input):
    prompt = generate_prompt(data)

    # ① Count prompt tokens before streaming (usage not in stream by default)
    #    We enable stream_options to get usage in the final chunk.
    stream = client.chat.completions.create(
        model="gpt-4o",
        stream=True,
        stream_options={"include_usage": True},   # ← gives usage in last chunk
        messages=[
            {
                "role": "system",
                "content": "You are a professional resume writer. Output plain text only."
            },
            {"role": "user", "content": prompt}
        ]
    )

    output_tokens = 0
    input_tokens  = 0

    for chunk in stream:
        # ── text chunk ──────────────────────────────────────────
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield sse("chunk", {"text": delta})

        # ── usage arrives in the LAST chunk ────────────────────
        if chunk.usage:
            input_tokens  = chunk.usage.prompt_tokens
            output_tokens = chunk.usage.completion_tokens

    # ② Send metadata as a final typed SSE event
    total_tokens = input_tokens + output_tokens
    total_price  = compute_price(input_tokens, output_tokens)

    yield sse("metadata", {
        "input_tokens":  input_tokens,
        "output_tokens": output_tokens,
        "total_tokens":  total_tokens,
        "total_price":   total_price,
        "model":         "gpt-4o"
    })

    yield sse("done", {})


# ── Route ─────────────────────────────────────────────────────────
@router.post("/generate/summary")
async def generate_summary(data: user_input):
    return StreamingResponse(
        stream_summary(data),
        media_type="text/event-stream",
        headers={
            "Cache-Control":    "no-cache",
            "X-Accel-Buffering": "no",      # disables Nginx buffering
            "Connection":       "keep-alive"
        }
    )
