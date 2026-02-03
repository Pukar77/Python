from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key =os.getenv("GEMINI_API_KEY")



client = genai.Client(api_key=api_key)



def generate():
    
    subtitle = "Nice, simple catch and drill this one. Keep the hands together out in front of the body, nice and strong. Keep the elbows nice and soft to allow to give with the ball. And just keep that head going towards the ball at all times. Head as still as possible, eyes on the ball."
    
    prompt = f"""
    
    
    """
    response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Explain how AI works in a paragraph",
    )
    print(response.text)
    
if __name__ == '__main__':
    generate()

