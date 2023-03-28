import openai

from config import OPENAI_API_KEY


def ChatGPT(messages):
    openai.api_key = OPENAI_API_KEY

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            *messages,
        ]
    )

    return completion['choices'][0]['message']["content"].strip()
