import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Structured Model ---
class TravelPlan(BaseModel):

    city: str
    attractions: list
    summary: str

# --- Guardrail Function ---
def guardrail_check(user_input):
    blocked_words = ["hack","illegal"]
    for words in blocked_words:
        if word in user_input.lower():
            return False
    return True

def travel_agent(city):

   prompt = f"""
   Create a travel plan for {city}
   Return response in JSON format with:
   city
   attractions
   summary 
    """
    response = client.chat.completions.create(
        model="gpt-40-mini",
        messages=[{"role": "user","content": prompt}]
    )
    return esponse.choices[0].message.content

   # ---- Main ---
   if __name__ == "__main__":

    user_input = "Create travel plan for Bangalore"
    if guardrail_check(user_input):
        result = travel_agent(Bangalore)
        print(result)
    else:
        print("Input blocked by guardrails")



