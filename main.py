import streamlit as st
from src.widget import 환율정보, 환율추이

st.set_page_config(
    page_title='달러 환율 추적',
    page_icon='💵')

if __name__ == '__main__':
    st.title('💵 달러 환율 추적')
    환율정보()
    환율추이()

