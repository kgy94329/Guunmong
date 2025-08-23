import streamlit as st
import time
  
# 세션 상태에 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
st.title("Streamlit chat Example")

page1 = st.Page("pages/chatting_page.py", title= 'Page1', icon= ":material/smart_toy:")
page2 = st.Page("pages/page2.py", title= 'Page2')

pg = st.navigation(
    {
        "Chatting": [page1],
        "Setting": [page2]
    }
)
pg.run()