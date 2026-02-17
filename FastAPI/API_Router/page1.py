from dotenv import load_dotenv
import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/info",
    tags=["Auto Generation"]
)

class UserInput(BaseModel):
    subtitle: str
    category: str


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

client = OpenAI(api_key=api_key)


@router.post("/generate")
def generate(text: UserInput):
    try:
        subtitle = text.subtitle.strip()
        category = text.category.strip()
        if not subtitle and category:
            raise ValueError("Subtitle Or Category is missing")

        prompt = f"""
       You are a senior instructional content writer and sports coaching analyst.

Your task is to transform raw video subtitles into high-quality educational metadata suitable for a professional learning or training platform.

Carefully read the subtitle and infer intent, focus, and skill complexity.
Do NOT add information that is not supported by the subtitle.

CONTENT GENERATION RULES
IMPORTANT RULES:

Output MUST be a single JSON object
Do NOT repeat any keys
Do NOT include markdown, code fences, or explanations
Do NOT output ```json or ```
Stop immediately after the closing brace

- Title

Short, clear, and engaging
Professional and instructional
Describe the main learning outcome
Avoid filler words and marketing language

- Description

3 to 5 well-written sentences
Explain what the drill or lesson teaches
Highlight key technique cues from the subtitle
Maintain a calm, confident coaching tone
Do NOT repeat the title verbatim

- Skills
CRITICAL: The user provides a category: "{category}"
You MUST select skills ONLY from the allowed list for this specific category.
NEVER create new skills. NEVER use skills from other categories. NEVER hallucinate.

ALLOWED SKILLS BY CATEGORY:

If category = "Mental Resilience":
  ONLY allowed skill: ["Mental Skills and Conditioning"]
  You MUST return exactly: ["Mental Skills and Conditioning"]

If category = "Nutrition":
  ONLY allowed skills: ["Hydration", "Meal Planning", "Recovery Nutrition", "Supplements", "General Nutrition"]
  Select 1 or more skills from this list based on subtitle content
  Example: ["Hydration", "Meal Planning"] or ["General Nutrition"]

If category = "Strength":
  ONLY allowed skills: ["Fitness", "Warm-up"]
  Select 1 or more skills from this list based on subtitle content
  Example: ["Fitness"] or ["Warm-up"] or ["Fitness", "Warm-up"]

If category = "Tactics":
  ONLY allowed skill: ["Strategy"]
  You MUST return exactly: ["Strategy"]

If category = "Technique":
  ONLY allowed skills: ["Batting", "Bowling", "Fielding", "Wicket Keeping", "Captaincy"]
  Select 1 or more skills from this list based on subtitle content
  Example: ["Batting"] or ["Batting", "Fielding"] or ["Wicket Keeping"]

STRICT ENFORCEMENT:
The category provided is: "{category}"
You can ONLY choose from the skills listed above for "{category}"
If the subtitle mentions multiple aspects, you may select multiple skills, but ONLY from the allowed list for "{category}"
DO NOT invent skills like "Bat Control", "Hand Placement", "Coordination", or any other skill not in the allowed list
If unsure which specific skills to pick, select the most general or relevant one from the allowed list

- Skill Level
Choose EXACTLY ONE:
Beginner, Easy, Intermediate, Advanced, Expert


OUTPUT FORMAT

Return EXACTLY this JSON structure and fill in the values.
Do not add, remove, or repeat keys.

{{
"content_title": "string",
"description": "string",
"skill": ["string"],
"skill_level": "Beginner | Easy | Intermediate | Advanced | Expert"
}}

SUBTITLE
{subtitle}

CRITICAL FINAL REMINDER - READ BEFORE GENERATING:
1. Category is: "{category}"
2. For "skill" field: ONLY use skills from the allowed list for category "{category}"
3. DO NOT create, invent, or hallucinate ANY skills

        """

        response = client.responses.create(
            model="gpt-4o",
            input=prompt,
        )

        if not response or not response.output_text:
            raise RuntimeError("Empty response from Gemini")

        llm_text = response.output_text.strip()

        try:
            parsed_output = json.loads(llm_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON returned by LLM: {llm_text}"
            ) from e

        return {
            "response": parsed_output
        }

    except ValueError as ve:
        # Client-side or validation errors
        return JSONResponse(
            status_code=400,
            content={
                "status" :0,
                "message": "Validation failed. Please check your input",
                "errors":{
                    "title":[str(ve)]
                }
                }  
        )

    except Exception as e: 
        # Catch EVERYTHING else so server never crashes
        return JSONResponse(
            status_code=500,
            content={
                "status":0,
                "message":"Internal Server error",
                "errors":{
                    "title":[str(e)]
                }
            }
          
        )
