import streamlit as st
import time
import datetime
import base64
from functions.tts_functions import get_synthesizer
from functions.llm_functions import create_response
import tempfile

ELEVENLABS_VOCAL_NAMES = [
    'Anna Kim', '고윤정', 'Taemin'
]

# 최초 실행 시만 설정
if "tts_model" not in st.session_state:
    st.session_state.tts_model = get_synthesizer('ElevenLabs', 'Anna Kim')

# 오디오 자동 재생 JS 생성 함수
def auto_play_audio(data):
    print('음성 출력')
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{data}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# 채팅 설정창
with st.popover(":material/instant_mix: 음성 설정"):
    model_option = st.selectbox("음성 모델 선택", ('Google', 'ElevenLabs'))
    vocal_option = ''
    if model_option == 'Google':
        vocal_option = st.selectbox("음성 선택", ('Kore'))
    else:  
        vocal_option = st.selectbox('음성 선택', ELEVENLABS_VOCAL_NAMES)

    if st.button('적용', type='primary'):
        st.session_state.tts_model = get_synthesizer(model_option, vocal_option)
        st.write(f'{model_option} 모델의 {vocal_option}이 적용되었습니다.')

# 채팅 기록 출력
for msg in st.session_state["messages"]:
    if msg['role'] == 'user':
        with st.chat_message('user'):
            st.markdown(msg['content'])
    else:
        with st.chat_message('assistant'):
            st.markdown(msg['content'])

# 입력창
if prompt := st.chat_input('메시지를 입력하세요...'):
    input_format = {'role': 'user', 'content': prompt}
    # 사용자 메시지 저장
    st.session_state['messages'].append(input_format)
    
    # 화면에 메시지 출력
    with st.chat_message('user'):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        print(f'[작업시작] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        placeholder = st.empty()
        placeholder.markdown("⏳ 음성 변환 중...")
        
        # GPT 답변 생성
        response = create_response(input_format)

        # 테스트 코드
        # response = prompt
        
        # 음성 합성
        tts_model = st.session_state.tts_model
        voice = tts_model.create_voice(response)
        
        print(f'[작업종료] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            
    # 챗봇 메시지 출력
    with st.chat_message('assistant'):
        def stream_date():
            for word in response.split(" "):
                yield word + " "
                time.sleep(0.02)
        placeholder.write_stream(stream_date)
        auto_play_audio(voice)
        
    # 챗봇 응답 저장
    st.session_state['messages'].append({'role': 'assistant', 'content': response})