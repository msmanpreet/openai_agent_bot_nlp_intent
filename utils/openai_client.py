import openai
import os

openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2023-05-15"

deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

async def ask_openai(prompt: str) -> str:
    response = openai.ChatCompletion.acreate(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": "You're a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']