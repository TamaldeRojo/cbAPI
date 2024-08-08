import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
MODEL = os.getenv('MODEL')


async def setup_openAi():
    API_KEY = os.getenv('OPENAI_API_KEY')
    api_key = API_KEY
    client = OpenAI()
    return client

async def get_gpt_Response(prompt: str,context: str):
    client = await setup_openAi()

    response = client.chat.completions.create(
                model=MODEL,
                temperature=0.5,
                max_tokens=100,
                messages=[
                    {"role":"system","content":context},
                    {"role":"user","content":prompt}
                    ],
            )
    res = response.choices[0].message.content
    
    return res