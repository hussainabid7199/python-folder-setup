from typing import List
import openai
from dotenv import load_dotenv
import os

dotenv_path = "backend\.env"
load_dotenv(dotenv_path=dotenv_path)

# openai
openai.api_key = os.getenv("OPEN_AI_API_KEY")
print(f"OpenAI API Key: {openai.api_key}")


def generate_answer_from_paragraphs(paragraphs: List[str], query: str) -> str:
    try:
        # Combine paragraphs into the context prompt
        prompt = f"Answer the following question based on the context:\n\n"
        prompt += "\n\n".join(paragraphs)
        prompt += f"\n\nQuestion: {query}\nAnswer:"

        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4000,
            temperature=0,
        )

        answer = response["choices"][0]["message"]["content"].strip()
        return answer

    except openai.RateLimitError:
        return "Error: Quota exceeded. Please check your plan and billing details."

    except Exception as e:
        return f"Error generating answer: {e}"
