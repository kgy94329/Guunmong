import streamlit as st
import time
import base64
from functions.tts_functions import create_voice
import tempfile

# 오디오 자동 재생 JS 생성 함수
def auto_play_audio():
    with open('data/response_voice.mp3', "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

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
    # 사용자 메시지 저장
    st.session_state['messages'].append({'role': 'user', 'content': prompt})
    
    # 화면에 메시지 출력
    with st.chat_message('user'):
        st.markdown(prompt)
    
    # 간단한 응답
    response = prompt

    with st.chat_message("assistant"):
        st.markdown(response)
        # TTS 변환 및 자동 재생
        tts = create_voice(response)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            auto_play_audio()
    # # 챗봇 메시지 출력
    # with st.chat_message('assistant'):
    #     def stream_date():
    #         for word in response.split(" "):
    #             yield word + " "
    #             time.sleep(0.02)
    #     st.write_stream(stream_date)
        
    # 챗봇 응답 저장
    st.session_state['messages'].append({'role': 'assistant', 'content': response})

