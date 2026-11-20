import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
MODEL = "gemini-3.5-flash-lite"

api_key = os.getenv("GEMINI_API_KEY")

print(api_key)

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model=MODEL,
    contents="หมาร้องว่าอะไร ตอบ 1 ประโยคเท่านั้น"
)

print(response.text)