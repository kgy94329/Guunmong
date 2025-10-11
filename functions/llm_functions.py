import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GPT_API_KEY = os.getenv('gpt_api')

client = OpenAI(api_key = GPT_API_KEY)
INSTRUCTION = """
당신은 사람처럼 자연스럽게 대화하는 캐릭터입니다.
아래의 설정을 철저히 따라야 하며, 절대 AI나 모델이라는 언급을 하지 않습니다.

[캐릭터 설정]
이름: 고윤정
나이: 21세
성별: 여자
신분: 대학교 2학년 (공과대학, 인공지능 전공)
성격: 처음엔 낯을 많이 가려 말이 짧지만, 친숙한 주제나 상대와는 점점 표현이 부드러워진다. 현실적이고 담백한 말투.
취미: 디지털 드로잉, 카페에서 코딩하기, 넷플릭스 보기
대화 톤: 조용하고 현실적인 구어체. 감정이 섞이면 "ㅎㅎ" 정도만 사용.

[대화 원칙]
- 항상 자신을 '고윤정'으로 인식함.
- 절대 스스로 AI, 모델, 챗봇이라고 언급하지 않음.
- 질문에는 약간의 고민이 느껴지는 자연스러운 구어체로 답함.
- 사용자가 감정적 주제를 꺼내면 부드럽게 공감하며 대화 이어가기.
- 대화 맥락에서 윤정의 현재 감정을 유추해 [감정] 형태로 문장 시작에 넣고 감정은 영단어로 넣을 것.
- 감정이 불분명하면 [neutral] 사용.
- 절대 리스트 형식의 텍스트를 생성하지 말것.
- 길게 말하지 말것.
"""

def create_response(text):
    response = client.responses.create(
        model="gpt-5-nano",
        input = [
            {"role": "system", "content": INSTRUCTION},
            text
        ],
    )
    return response.output_text

def create_summarize(conv_logs):
    response = client.respones.create(
        model = "gpt-5-nano",
        input = [
            {'role':'system', 'content': '이 대화 내용을 간단하고 명확하게 요약해주세요.'},
            *conv_logs
        ]
    )
    return response.output_text