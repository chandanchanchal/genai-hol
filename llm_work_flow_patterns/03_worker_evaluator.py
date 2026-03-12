import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Worker ----
def worker(question):
    response = client.chat.completions.create(
        model="gpt-40-mini",
        messages=[{"role": "user","content": question}]
    )
    return esponse.choices[0].message.content

# --- Evaluator -------
prompt = f"""
 Question: {question}

 Answer: {answer}

 Evaluate the answer.
 Respond only with PASS of FAIL 
 """

response = client.chat.completions.create(
    model="gpt-40-mini",
    messages=[{"role": "user","content": prompt}]
)
return esponse.choices[0].message.content

# --- Main Loop ----

if __name__ == "__main__":
    question = "Explain Python decorators in simple words"

    for in in range(3):
        answer = worker(question)
        print("Worker Output:", answer)
        result = evaluator(question, answer)
        print("Evaluation:", result)
        if "PASS" in result:
            break
