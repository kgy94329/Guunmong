import streamlit as st
import time
import datetime
import base64
from functions.tts_functions import create_voice
from functions.llm_functions import create_response
import tempfile

# 오디오 자동 재생 JS 생성 함수
def auto_play_audio(data):
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{data}" type="audio/mp3">
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
    # response = prompt
    

    with st.chat_message("assistant"):
        print(f'[작업시작] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        placeholder = st.empty()
        placeholder.markdown("⏳ 음성 변환 중...")
        
        # GPT 답변 생성
        response = create_response(prompt)
        
        # 음성 합성
        tts = create_voice(response)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            auto_play_audio(tts)
        print(f'[작업종료] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            
    # 챗봇 메시지 출력
    with st.chat_message('assistant'):
        def stream_date():
            for word in response.split(" "):
                yield word + " "
                time.sleep(0.02)
        placeholder.write_stream(stream_date)
        
    # 챗봇 응답 저장
    st.session_state['messages'].append({'role': 'assistant', 'content': response})
