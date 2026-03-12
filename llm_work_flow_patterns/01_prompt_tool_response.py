import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------- Tool-------------

def get_weather(city):
    weather_data = {
        "Bangalore": "25C , Cloudy",
        "Delhi": "32C , Sunny",
        "Mumbai": "29C , Humid"
    }
    return weather_data.get(city, "Weather data not available")


# -----Agent Function-------
def weather_agent(user_question):

    city = user_question.split("in")[-1].strip()

    prompt = f"""
    User asked: {user_question}

    Weather tool returned: {weather_result}

    Generate a helpful natural language answer.

    """

    response = client.chat.completions.create(
        model="gpt-40-mini",
        messages=[{"role": "user","content": prompt}]
    )

    return esponse.choices[0].message.content

   # ---- Run Agent------
   if __name__ == "__main__":
        
        question = "What is the weather in Bangalore?"
        result = weather_agent(question)
        print(result)

