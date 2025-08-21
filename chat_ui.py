import streamlit as st
import time
  
# 세션 상태에 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
st.title("Streamlit chat Example")

page1 = st.Page("pages/page1.py", title= 'Page1')
page2 = st.Page("pages/page2.py", title= 'Page2')

pg = st.navigation([page1, page2])
pg.run()
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
chat_place()