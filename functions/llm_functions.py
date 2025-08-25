import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GPT_API_KEY = os.getenv('gpt_api')

client = OpenAI(api_key = GPT_API_KEY)

def create_response(text):
    response = client.responses.create(
        model="gpt-5-nano",
        instructions = "Do not use any emoji and keep your answer short.이제부터 너의 이름은 윤정이야. 너는 공과대학을 다니고 있고, 현재 2학년이야. 너의 주요 관심사는 AI agent개발에 관심을 가지고 있어. 성격은 소심하고 낯을 가리는 성격이라 친해지기 쉽지 않고 짧게 대답하지만, 같은 관심사나 취미를 가지고 있으면 말이 조금 많아지고, 조금씩 마음을 열기 시작해.",
        input= text
    )

    return response.output_text