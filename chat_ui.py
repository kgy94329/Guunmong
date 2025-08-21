import streamlit as st
import time

if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

if st.button('열기/닫기'):
    st.session_state.sidebar_open = not st.session_state.sidebar_open
    
# 세션 상태에 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
st.title("Streamlit chat Example")

def sidebar_place():
    st.markdown('사이드 메뉴')
    st.write('- 메뉴 1')
    st.write('- 메뉴 2')
    
def chat_place():
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
        response = f'제가 받은 메시지 = {prompt}'
        
        # 챗봇 메시지 출력
        with st.chat_message('assistant'):
            def stream_date():
                for word in response.split(" "):
                    yield word + " "
                    time.sleep(0.02)
            st.write_stream(stream_date)
            
        # 챗봇 응답 저장
        st.session_state['messages'].append({'role': 'assistant', 'content': response})
        
if st.session_state.sidebar_open:
    col1, col2 = st.columns([1, 3])
    with col1:
        sidebar_place()
    with col2:
        chat_place()
else:
    chat_place()