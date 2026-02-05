from dotenv import load_dotenv
import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter(
    prefix="/info",
    tags=["Auto Generation"]
)

class UserInput(BaseModel):
    subtitle: str


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

client = OpenAI(api_key=api_key)


@router.post("/generate")
def generate(text: UserInput):
    try:
        subtitle = text.subtitle.strip()
        if not subtitle:
            raise ValueError("Subtitle cannot be empty")

        prompt = f"""
        You are a senior instructional content writer and sports coaching analyst.

    Your task is to transform raw video subtitles into high-quality educational metadata suitable for a professional learning or training platform.

    Carefully read the subtitle and infer intent, focus, and skill complexity.
    Do NOT add information that is not supported by the subtitle.


    CONTENT GENERATION RULES
    IMPORTANT RULES:
    - Output MUST be a single JSON object
    - Do NOT repeat any keys
    - Do NOT include markdown, code fences, or explanations
    - Do NOT output ```json or ```
    - Stop immediately after the closing brace 


    1. Title
    - Short, clear, and engaging
    - Professional and instructional
    - Describe the main learning outcome
    - Avoid filler words and marketing language

    2. Description
    - 3 to 5 well-written sentences
    - Explain what the drill or lesson teaches
    - Highlight key technique cues from the subtitle
    - Maintain a calm, confident coaching tone
    - Do NOT repeat the title verbatim

    3. Skills
    - List the primary skills demonstrated or trained
    - Use concise, clear skill names
    - Avoid overly generic terms

    4. Skill Level
    Choose EXACTLY ONE:
    Beginner, Easy, Intermediate, Advanced, Expert

    5. Tags
    - Select EXACTLY 5 tags

    - Tags MUST come ONLY from the provided allowed tags list

    - Choose the tags that most accurately reflect:

    - The core technique

    - The specific skill focus

    - The context of execution

    - Do NOT select tags based on name similarity alone

    - Do NOT invent, modify, or duplicate tags

    ALLOWED TAGS:
    Grip and Stance, Footwork and Timing, Shot Selection, Running Between Wickets, Forward Defense, Back Defense, Leaving the Ball, Cover Drive, Straight Drive, Off Drive, On Drive, Cut Shot, Square Cut, Late Cut, Pull Shot, Hook Shot, Back Foot Punch, Leg Glance, Flick Shot, Sweep Shot, Paddle Sweep, Defensive Strokes, Cover Drive, Straight Drive, On Drive, Square Drive, Pull Shot, Hook Shot, Cut Shot, Glance, Flick, Reverse Sweep, Scoop Shot, Switch Hit, Helicopter Shot, Reverse Sweep, Scoop Shot, Switch Hit, Helicopter Shot, Run-up and Delivery, Line and Length, Swing Bowling, Seam Bowling, Slower Balls and Cutters, Bouncers and Yorkers, Off-Spin, Leg-Spin, Left-Arm Spin, Outswinger, Inswinger, Yorker, Bouncer, Slower Ball, Off Cutter, Knuckle Ball, Leg Cutter, Off Break, Leg Break, Doosra, Googly, Top Spinner, Flipper, Arm Ball, Slider, High Catching, Diving Catch, Slip Catching, Reflex Catching, Sliding Stop, Dive Stop, Pick Up and Throw, Direct Hit, Flat Throw, Relay Throwing, Fielding Positions, Slip Fielding, Gully Fielding, Point Fielding, Cover Fielding, Mid-Wicket Fielding, Boundary Fielding, Keeper Stance, Keeper Footwork, Taking Pace Bowling, Taking Spin Bowling, Diving Take, Leg Side Stumping, Off Side Stumping, Run Out Techniques, Wicketkeeper Stance, Glovework, Wicketkeeper Footwork, Reading the Pitch, Weather & Overhead Conditions, Batting First Strategy, Bowling First Strategy, Pitch Evolution Understanding, Opening Partnership Selection, Middle Order Construction, Death Overs Specialists, Pinch Hitter / Promoted Batsman, Nightwatchman Strategy, Batsman-Bowler Matchups, Opening Bowling Strategy, First Change Bowler, Introducing Spin Bowling, Bowling Matchup Strategy, Death Bowling Management, New Ball Strategy, Over Rate Management, Attacking Field Settings, Defensive Field Settings, Powerplay Restrictions, Field Settings for Pace, Field Settings for Spin, Death Overs Field Placements, Umbrella Field (Catching Arc), On-Field Communication, Team Motivation & Morale, Managing Different Personalities, Leading Under Pressure, Strategic Timeouts, Player Rotation & Workload, Post-Match Reflection, Recognizing Momentum Shifts, DRS & Review Strategy, Breaking Partnerships, Run Rate Management, Chasing Strategy, Declaration Timing, Shoulder Mobility, Arm Circles, Shoulder and Spine Mobility, Shoulder Stretches, Forearm Curls, Shadow Batting, Batting Lunges, Medicine Ball Slams, Chest & Back, Squat Pulses, Hip and Ankle Mobility, Core Rotation Drills, Balance & Stability, Abdominal Strength, Thoracic Rotation, Twist Band Pulls, Core Stability, Dynamic Stretching, Groin and Inner Thigh Stretches, Hip Mobility, Weighted Bat Drives, Ball Reaction Drills, Wrist Extenders, High Intensity Training, Wrist Icing, Match Scenario Visualization, Skill Reinforcement Imagery, Box Breathing, Pranayama, Mindfulness Meditation, Thought Labeling, Concentration Grids, Mental Cue Words, Positive Self-Talk, Success Journaling, Simulated Pressure Drills, Post-Game Reflection, Balanced Whole Foods, Meal Timing, Sleep-Supporting Nutrients, Carb Loading, Baseline Hydration, Electrolyte Drinks, Quick Energy, Protein Intake, Anti-Inflammatory Foods, Creatine, Caffeine, Omega-3, Urine Color Monitoring, Hydration Checklists

    ────────────────────
    OUTPUT FORMAT
    ────────────────────

    Return EXACTLY this JSON structure and fill in the values.
    Do not add, remove, or repeat keys.

    {{
    "content_title": "string",
    "description": "string",
    "skill": ["string"],
    "skill_level": "Beginner | Easy | Intermediate | Advanced | Expert",
    "tags": ["string"]
    }}

    ────────────────────
    SUBTITLE
    ────────────────────
    <<<
    {subtitle}
    >>>
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
        raise HTTPException(
            status_code=400,
            detail=str(ve)
        )

    except Exception as e:
        # Catch EVERYTHING else so server never crashes
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
