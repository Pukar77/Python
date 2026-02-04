from google import genai
from dotenv import load_dotenv
import os
import json
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/info",
    tags=["Auto Generation"]
)

class userInput(BaseModel):
    subtitle:str
    

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def extract_name(nodes):
    results=[]
    for node in nodes:
        children = node.get("children", [])

        # ✅ leaf node condition
        if isinstance(children, list) and len(children) == 0:
            name = node.get("name")
            description = node.get("description")
            if name:
                results.append({
                    "name":name,
                    "description":description
                    })
                

        # 🔁 keep traversing if children exist
        elif isinstance(children, list):
            results.extend(extract_name(children))
    # print(len(results))
    return results
   

@router.post("/generate")
def generate(text: userInput):
    with open("hehe.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    subtitle = text.subtitle

    # Extract taxonomy names for allowed tags
    # allowed_tags = extract_name(raw_data["data"])
    # print(allowed_tags)
    
    allowed_tags = [{'name': 'Grip and Stance', 'description': 'Foundation of batting technique'}, {'name': 'Footwork and Timing', 'description': 'Movement and timing principles'}, {'name': 'Shot Selection', 'description': 'Choosing the right shot for match situation'}, {'name': 'Running Between Wickets', 'description': 'Effective running and communication'}, {'name': 'Forward Defense', 'description': 'Classic defensive stroke played with a full extension, bat and pad together'}, {'name': 'Back Defense', 'description': 'Defensive stroke played on the back foot, staying tall and watching the ball onto the bat'}, {'name': 'Leaving the Ball', 'description': 'Technique of judging line and length to safely leave deliveries outside off stump'}, {'name': 'Cover Drive', 'description': 'Attacking stroke played with full extension through the cover region'}, {'name': 'Straight Drive', 'description': 'The most elegant cricket stroke, played straight back past the bowler with full face of the bat'}, {'name': 'Off Drive', 'description': 'Attacking drive through the off-side between cover and mid-off'}, {'name': 'On Drive', 'description': 'Front foot drive played through mid-on with wrists rolling over'}, {'name': 'Cut Shot', 'description': 'Horizontal bat stroke played on the back foot through the point region'}, {'name': 'Square Cut', 'description': 'Cut shot played squarer, perpendicular to the pitch'}, {'name': 'Late Cut', 'description': 'Delicate cut played very late, guiding the ball fine past the keeper'}, {'name': 'Pull Shot', 'description': 'Attacking horizontal bat stroke played to short-pitched deliveries on the leg side'}, {'name': 'Hook Shot', 'description': 'Aggressive stroke to bouncer-length balls, hitting the ball high and square on the leg side'}, {'name': 'Back Foot Punch', 'description': 'Controlled stroke played on the back foot with a straight bat through the off side'}, {'name': 'Leg Glance', 'description': 'Delicate deflection of the ball on the leg side using the pace of the delivery'}, {'name': 'Flick Shot', 'description': 'Wristy stroke played by closing the bat face and flicking through mid-wicket'}, {'name': 'Sweep Shot', 'description': 'Attacking stroke against spin, played from a kneeling position sweeping the ball square'}, {'name': 'Paddle Sweep', 'description': 'Delicate sweep played very fine, using the pace of the ball'}, {'name': 'Defensive Strokes', 'description': 'Forward and backward defense'}, {'name': 'Cover Drive', 'description': 'Classic front foot shot through covers'}, {'name': 'Straight Drive', 'description': 'The purest cricket shot down the ground'}, {'name': 'On Drive', 'description': 'Front foot shot through mid-on'}, {'name': 'Square Drive', 'description': 'Powerful shot through point region'}, {'name': 'Pull Shot', 'description': 'Horizontal bat shot to leg-side'}, {'name': 'Hook Shot', 'description': 'Aggressive shot to short-pitched balls'}, {'name': 'Cut Shot', 'description': 'Backfoot shot square on off-side'}, {'name': 'Glance', 'description': 'Delicate deflection to fine leg'}, {'name': 'Flick', 'description': 'Wristy shot through mid-wicket'}, {'name': 'Reverse Sweep', 'description': 'Pre-meditated stroke reversing the grip to play on the off side against spin'}, {'name': 'Scoop Shot', 'description': 'Playing the ball from outside off stump over the keeper using an angled bat face'}, {'name': 'Switch Hit', 'description': 'Changing batting stance completely mid-delivery to convert off to leg side and vice versa'}, {'name': 'Helicopter Shot', 'description': 'Powerful wristy stroke with a complete follow-through, bat rotating like helicopter blades'}, {'name': 'Reverse Sweep', 'description': 'Pre-meditated stroke reversing the grip to play on the off side against spin'}, {'name': 'Scoop Shot', 'description': 'Playing the ball from outside off stump over the keeper using an angled bat face'}, {'name': 'Switch Hit', 'description': 'Changing batting stance completely mid-delivery to convert off to leg side and vice versa'}, {'name': 'Helicopter Shot', 'description': 'Powerful wrist-driven shot'}, {'name': 'Run-up and Delivery', 'description': 'Bowling action fundamentals'}, {'name': 'Line and Length', 'description': 'Bowling accuracy and control'}, {'name': 'Swing Bowling', 'description': 'Conventional and reverse swing'}, {'name': 'Seam Bowling', 'description': 'Using the seam for deviation'}, {'name': 'Slower Balls and Cutters', 'description': 'Deceptive pace variations'}, {'name': 'Bouncers and Yorkers', 'description': 'Attacking length variations'}, {'name': 'Off-Spin', 'description': 'Finger spin turning into right-hander'}, {'name': 'Leg-Spin', 'description': 'Wrist spin turning away from right-hander'}, {'name': 'Left-Arm Spin', 'description': 'Orthodox left-arm spin'}, {'name': 'Outswinger', 'description': 'Delivery that swings away from the batsman in the air, using seam position and wrist angle'}, {'name': 'Inswinger', 'description': 'Delivery that swings into the batsman, targeting pads and stumps'}, {'name': 'Yorker', 'description': "Full-length delivery aimed at the batsman's toes, extremely effective at the death"}, {'name': 'Bouncer', 'description': "Short-pitched intimidatory delivery directed at the batsman's head or upper body"}, {'name': 'Slower Ball', 'description': 'Deceptive change of pace delivery using variations in grip and release'}, {'name': 'Off Cutter', 'description': 'Delivery that cuts away from right-handed batsman after pitching, using finger position'}, {'name': 'Knuckle Ball', 'description': 'Slower delivery gripped with knuckles instead of fingers, reducing pace significantly'}, {'name': 'Leg Cutter', 'description': 'Delivery that cuts into right-handed batsman, opposite to off-cutter'}, {'name': 'Off Break', 'description': "Off-spinner's stock delivery that turns from off to leg for right-handed batsman"}, {'name': 'Leg Break', 'description': "Leg-spinner's stock ball spinning from leg to off for right-handed batsman"}, {'name': 'Doosra', 'description': "Off-spinner's variation that spins the opposite way (leg to off), the other one in Urdu"}, {'name': 'Googly', 'description': "Leg-spinner's wrong'un, spinning from off to leg like an off-break"}, {'name': 'Top Spinner', 'description': 'Delivery with over-spin causing the ball to dip and bounce more than expected'}, {'name': 'Flipper', 'description': 'Back-spinning delivery squeezed out of fingers, skidding low with extra pace'}, {'name': 'Arm Ball', 'description': 'Delivery that goes straight on with the arm instead of spinning'}, {'name': 'Slider', 'description': 'Faster delivery with minimal spin, skidding through low'}, {'name': 'High Catching', 'description': 'Taking catches above head height, often under pressure near the boundary'}, {'name': 'Diving Catch', 'description': 'Full-extension diving catches requiring commitment and technique'}, {'name': 'Slip Catching', 'description': 'Specialist catching technique for edges, requiring soft hands and reflexes'}, {'name': 'Reflex Catching', 'description': 'Instinctive catches at close positions requiring lightning reflexes'}, {'name': 'Sliding Stop', 'description': 'Dynamic sliding technique to stop the ball and prevent boundaries'}, {'name': 'Dive Stop', 'description': 'Full-length diving to stop powerful strokes in the inner circle'}, {'name': 'Pick Up and Throw', 'description': 'Clean gathering and quick release for run-out attempts'}, {'name': 'Direct Hit', 'description': 'Throwing directly at stumps from any angle or distance for run-outs'}, {'name': 'Flat Throw', 'description': 'Low trajectory powerful throw from the deep to minimize travel time'}, {'name': 'Relay Throwing', 'description': 'Coordinated throwing between fielders to quickly return the ball from deep'}, {'name': 'Fielding Positions', 'description': 'Specific position skills'}, {'name': 'Slip Fielding', 'description': 'Specialist position standing beside the keeper to catch edges'}, {'name': 'Gully Fielding', 'description': 'Close catching position between slips and point'}, {'name': 'Point Fielding', 'description': 'Athletic position saving runs on the off-side, requiring quick reflexes'}, {'name': 'Cover Fielding', 'description': 'Key attacking position requiring excellent ground fielding and throwing'}, {'name': 'Mid-Wicket Fielding', 'description': 'Central leg-side position, often requiring quick reactions to powerful strokes'}, {'name': 'Boundary Fielding', 'description': 'Deep fielding requiring powerful throws and good judgment of catches near the rope'}, {'name': 'Keeper Stance', 'description': 'Proper crouching position allowing quick movement in any direction'}, {'name': 'Keeper Footwork', 'description': 'Quick and efficient movement patterns following the ball'}, {'name': 'Taking Pace Bowling', 'description': 'Clean collection technique for fast bowling with soft hands'}, {'name': 'Taking Spin Bowling', 'description': 'Standing up to stumps for spin, requiring quick hands and anticipation'}, {'name': 'Diving Take', 'description': 'Full-stretch diving catches to prevent byes and take edges'}, {'name': 'Leg Side Stumping', 'description': 'Quick stumping technique for balls down the leg side'}, {'name': 'Off Side Stumping', 'description': 'Stumping on the off side requiring clean collection and quick hands'}, {'name': 'Run Out Techniques', 'description': 'Quick gathering and breaking stumps for run-out opportunities'}, {'name': 'Wicketkeeper Stance', 'description': 'Proper stance and readiness position'}, {'name': 'Glovework', 'description': 'Clean catching and handling'}, {'name': 'Wicketkeeper Footwork', 'description': 'Movement and positioning'}, {'name': 'Reading the Pitch', 'description': 'Assessing pitch characteristics, moisture, grass cover, cracks, and expected behavior'}, {'name': 'Weather & Overhead Conditions', 'description': 'Understanding cloud cover, humidity, wind, and their impact on swing and seam'}, {'name': 'Batting First Strategy', 'description': 'When to bat first: flat pitches, winning toss in Tests, setting targets in limited overs'}, {'name': 'Bowling First Strategy', 'description': 'When to bowl first: seaming conditions, chasing mentality, dew factor in night games'}, {'name': 'Pitch Evolution Understanding', 'description': 'Predicting how the pitch will play over time: day 1-5 in Tests, dew effect in white-ball'}, {'name': 'Opening Partnership Selection', 'description': 'Choosing openers for different formats: technique vs aggression balance'}, {'name': 'Middle Order Construction', 'description': 'Building stability with accumulators and power-hitters at positions 3-6'}, {'name': 'Death Overs Specialists', 'description': 'Selecting and positioning finishers for explosive endings in limited overs cricket'}, {'name': 'Pinch Hitter / Promoted Batsman', 'description': 'Promoting lower-order batsmen for power-play advantage or momentum shift'}, {'name': 'Nightwatchman Strategy', 'description': 'When to use a nightwatchman in Test cricket to protect top-order batsmen'}, {'name': 'Batsman-Bowler Matchups', 'description': 'Manipulating batting order to exploit favorable matchups and avoid difficult bowlers'}, {'name': 'Opening Bowling Strategy', 'description': 'Selecting opening bowlers based on conditions: swing, seam, or pace attack'}, {'name': 'First Change Bowler', 'description': 'When to introduce first change bowler: after powerplay, when openers tire, or matchups'}, {'name': 'Introducing Spin Bowling', 'description': 'Timing spin introduction based on pitch, match situation, and batsman comfort'}, {'name': 'Bowling Matchup Strategy', 'description': 'Exploiting batsman weaknesses: right-arm over to left-hand bat, short ball to tailenders'}, {'name': 'Death Bowling Management', 'description': 'Rotating yorker specialists, wide variations, and managing overs in final phase'}, {'name': 'New Ball Strategy', 'description': 'Taking second new ball in Tests, managing overs to have best bowlers ready'}, {'name': 'Over Rate Management', 'description': 'Balancing bowling changes and field settings to maintain required over rate'}, {'name': 'Attacking Field Settings', 'description': 'Setting aggressive fields with close catchers to pressure batsmen and create wickets'}, {'name': 'Defensive Field Settings', 'description': 'Protecting boundaries and restricting scoring when wickets are not falling'}, {'name': 'Powerplay Restrictions', 'description': 'Maximizing attacking fields within powerplay restrictions in limited overs formats'}, {'name': 'Field Settings for Pace', 'description': 'Setting fields for fast bowlers based on ball condition, pitch, and batsman strengths'}, {'name': 'Field Settings for Spin', 'description': 'Specific fields for off-spinners, leg-spinners in different match situations'}, {'name': 'Death Overs Field Placements', 'description': 'Strategic boundary protection while maintaining wicket-taking options in final overs'}, {'name': 'Umbrella Field (Catching Arc)', 'description': 'Ring of close catchers around the bat for new batsmen or turning pitches'}, {'name': 'On-Field Communication', 'description': 'Clear communication with bowlers, fielders, and wicketkeeper about plans and adjustments'}, {'name': 'Team Motivation & Morale', 'description': 'Keeping team motivated during difficult periods, celebrating small wins, positive body language'}, {'name': 'Managing Different Personalities', 'description': 'Handling star players, young players, and difficult personalities in the team'}, {'name': 'Leading Under Pressure', 'description': 'Staying calm and making clear decisions when the game is on the line'}, {'name': 'Strategic Timeouts', 'description': 'Using timeouts effectively to regroup, break partnerships, or plan strategies'}, {'name': 'Player Rotation & Workload', 'description': 'Managing bowler workloads, resting key players, balancing short and long-term goals'}, {'name': 'Post-Match Reflection', 'description': 'Analyzing decisions, learning from wins and losses, continuous improvement'}, {'name': 'Recognizing Momentum Shifts', 'description': 'Identifying when momentum is shifting and taking action to counter or capitalize'}, {'name': 'DRS & Review Strategy', 'description': 'Strategic use of reviews: saving reviews, challenging umpire calls at key moments'}, {'name': 'Breaking Partnerships', 'description': 'Tactics to break dangerous partnerships: bowling changes, field changes, pressure building'}, {'name': 'Run Rate Management', 'description': 'Controlling scoring rate in middle overs, building pressure through dot balls'}, {'name': 'Chasing Strategy', 'description': 'Managing run chases: calculating required rates, batting powerplay, wickets in hand'}, {'name': 'Declaration Timing', 'description': 'When to declare in Test cricket to give bowlers time while ensuring enough runs'}, {'name': 'Shoulder Mobility', 'description': 'Prepare shoulders for high catches'}, {'name': 'Arm Circles', 'description': 'Prepare shoulders for bowling'}, {'name': 'Shoulder and Spine Mobility', 'description': 'Prevent injury and improve bowling action'}, {'name': 'Shoulder Stretches', 'description': 'Improve shoulder mobility for cover drive execution'}, {'name': 'Forearm Curls', 'description': 'Build forearm strength for powerful cover drives'}, {'name': 'Shadow Batting', 'description': 'Warm-up with shadow batting movements'}, {'name': 'Batting Lunges', 'description': 'Leg strength warm-up for front foot shots'}, {'name': 'Medicine Ball Slams', 'description': 'Power warm-up for pull shot execution'}, {'name': 'Chest & Back', 'description': 'Chest and back strengthening exercises'}, {'name': 'Squat Pulses', 'description': 'Build leg strength for wicketkeeping'}, {'name': 'Hip and Ankle Mobility', 'description': 'Leg-spin pivot preparation'}, {'name': 'Core Rotation Drills', 'description': 'Develop explosive core rotation for pull shots'}, {'name': 'Balance & Stability', 'description': 'Balance and stability exercises'}, {'name': 'Abdominal Strength', 'description': 'Abdominal strengthening exercises'}, {'name': 'Thoracic Rotation', 'description': 'Upper body mobility for hook shots'}, {'name': 'Twist Band Pulls', 'description': 'Rotational power development'}, {'name': 'Core Stability', 'description': 'Core stability and anti-rotation exercises'}, {'name': 'Dynamic Stretching', 'description': 'Dynamic stretching and warm-up movements'}, {'name': 'Groin and Inner Thigh Stretches', 'description': 'Flexibility for on drive positioning'}, {'name': 'Hip Mobility', 'description': 'Maintain wicketkeeping stance endurance'}, {'name': 'Weighted Bat Drives', 'description': 'Build strength with weighted bat practice'}, {'name': 'Ball Reaction Drills', 'description': 'Improve reaction time and hand-eye coordination'}, {'name': 'Wrist Extenders', 'description': 'Wrist flexibility for straight drive timing'}, {'name': 'High Intensity Training', 'description': 'High intensity interval training'}, {'name': 'Wrist Icing', 'description': 'Recovery protocol for wrist health'}, {'name': 'Match Scenario Visualization', 'description': 'Mentally rehearse match situations'}, {'name': 'Skill Reinforcement Imagery', 'description': 'Visualize perfect technique execution'}, {'name': 'Box Breathing', 'description': '4-4-4-4 breathing pattern for stress management'}, {'name': 'Pranayama', 'description': 'Yogic breathing techniques'}, {'name': 'Mindfulness Meditation', 'description': 'Present-moment awareness practice'}, {'name': 'Thought Labeling', 'description': 'Identify and reframe negative thoughts'}, {'name': 'Concentration Grids', 'description': 'Number grid focus exercises'}, {'name': 'Mental Cue Words', 'description': 'Personal trigger words for focus'}, {'name': 'Positive Self-Talk', 'description': 'Daily affirmations for confidence'}, {'name': 'Success Journaling', 'description': 'Document and reflect on past wins'}, {'name': 'Simulated Pressure Drills', 'description': 'Practice in high-pressure training'}, {'name': 'Post-Game Reflection', 'description': 'Learn from performance experiences'}, {'name': 'Balanced Whole Foods', 'description': 'Carbs, protein, and healthy fats'}, {'name': 'Meal Timing', 'description': 'Optimize nutrient timing around training'}, {'name': 'Sleep-Supporting Nutrients', 'description': 'Foods that aid recovery sleep'}, {'name': 'Carb Loading', 'description': 'Complex carbohydrates 12-24 hours before'}, {'name': 'Baseline Hydration', 'description': 'Pre-match hydration checks'}, {'name': 'Electrolyte Drinks', 'description': 'Replace lost salts during breaks'}, {'name': 'Quick Energy', 'description': 'Fruit, gels, energy bars'}, {'name': 'Protein Intake', 'description': '30-minute window for muscle repair'}, {'name': 'Anti-Inflammatory Foods', 'description': 'Turmeric, berries, omega-3 sources'}, {'name': 'Creatine', 'description': 'Strength and power support'}, {'name': 'Caffeine', 'description': 'Pre-match alertness booster'}, {'name': 'Omega-3', 'description': 'Joint health and inflammation reduction'}, {'name': 'Urine Color Monitoring', 'description': 'Simple hydration status check'}, {'name': 'Hydration Checklists', 'description': 'Before, during, and after activity'}]



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

- Each tag must be selected by evaluating BOTH its name AND its description

- Choose the tags that most accurately reflect:

- The core technique

- The specific skill focus

- The context of execution

- Do NOT select tags based on name similarity alone

- Do NOT invent, modify, or duplicate tags

────────────────────
OUTPUT FORMAT
────────────────────

Return EXACTLY this JSON structure and fill in the values.
Do not add, remove, or repeat keys.

{{
  "title": "string",
  "description": "string",
  "skills": ["string"],
  "skill_level": "Beginner | Easy | Intermediate | Advanced | Expert",
  "tags": ["string"]
}}

────────────────────
SUBTITLE
────────────────────
<<<
{subtitle}
>>>

────────────────────
ALLOWED TAGS
────────────────────
{allowed_tags}

"""

    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt,
    )

    # print(response.text)
    
    llm_text = response.text.strip()
    try:
        parsed_output = json.loads(llm_text)
    except json.JSONDecodeError:
        return{
            "error":"Failed to parse the output",
            "response":response.text
        }
    return{
        "response":parsed_output,
        } 


# if __name__ == "__main__":
#     raw_data = generate()
#     datas = extract_name(raw_data["data"])
    # print(json.dumps(datas, indent=2))
