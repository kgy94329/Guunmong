import streamlit as st
import time
  
# 세션 상태에 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
st.title("Streamlit chat Example")

page1 = st.Page("pages/chatting_page.py", title= 'AI chatbot', icon= ":material/smart_toy:")
page2 = st.Page("pages/storytelling_page.py", title= 'AI Storytelling', icon= ":material/auto_stories:")

pg = st.navigation(
    {
        "Chatting": [page1],
        "Storytelling": [page2]
    }
)
pg.run()