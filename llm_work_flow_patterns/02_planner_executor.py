import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Tools -------

def search_place(city):
    return f"Top attractions in {city}: Lalbagh ,Cubbon Park, Bangalore Palace "

def get_weather(city):
    return f"Weather in {city}: 25 C Cloudy"

#-----Planner -----

def planner(user_request)
    prompt = f""" 
    Break the following request into steps:
    Request: {user_request}
    Output steps as numbered list.
    """
    response = client.chat.completions.create(
        model="gpt-40-mini",
        messages=[{"role": "user","content": prompt}]
    )

    return esponse.choices[0].message.content

    # ---- Executor --------
    def executor(plan,city):
        results = []
        for step in plan.split("\n"):
            if "attraction" in step.lower():
                results.append(search_places(city))
            elif "weather" in step.lower():
                results.append(get_weather(city))
        return results

   # ---- Run Main------
   if __name__ == "__main__":
        
        request = "Create a travel summery for Bangalore"
        plan = planner(request)
        print("Generate Plan: ")
        print(plan)

        execution_results = executor(plan, "Bangalore")
        print("\nExecution Results:")
        print(execution_results)