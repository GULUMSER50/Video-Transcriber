from openai import OpenAI
from config import OPENAI_API_KEY, TRANSLATION_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def translate_text(text, target_language):
    print(f"Starting translation to {target_language}")
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}."},
            {"role": "user", "content": text}
        ]
    )
    print(f"Translation to {target_language} completed")
    return response.choices[0].message.content