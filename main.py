import streamlit as st
from src.data import 은행고시환율_가져오기, 야후파이낸스환율_가져오기, 야후파이낸스환율추이_가져오기
import plotly.express as px

st.set_page_config(
    page_title='달러 환율 추적',
    page_icon='💵')
st.title('💵 달러 환율 추적')

with st.container(border=True):
    st.header('ℹ️ 환율 정보')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('은행 고시 환율')
        은행고시환율 = 은행고시환율_가져오기()
        st.metric('환율(원)', 은행고시환율.get('basePrice'))
        dt = 은행고시환율.get('date') + ' ' + 은행고시환율.get('time')
        st.caption(f'업데이트 기준 : {dt}')
    야후파이낸스환율 = 야후파이낸스환율_가져오기()
    with col2:
        st.subheader('야후 파이낸스 환율')
        st.metric('환율(원)', f'{float(야후파이낸스환율.iloc[-1]["Close"]):.2f}')
        st.caption(f'업데이트 기준 : {야후파이낸스환율.index[-1].strftime("%Y-%m-%d %H:%M:%S")}')
    if st.button('🔄 데이터 최신화', use_container_width=True):
        st.rerun()
with st.container(border=True):
    st.header('📈 환율 추이')
    col1, col2, col3 = st.columns(3)
    def 버튼작동(key, n):
        st.session_state[key] = n
    버튼 = lambda x, y, z : x.button(f'{z}', on_click=lambda : 버튼작동(y, z), use_container_width=True)
    with col1:
        category = '기간'
        st.slider(category, 50, 500, 200, 1, key=category)
        for col, val in zip(st.columns(3), [50, 100, 200]):
            버튼(col, category, val)
    with col2:
        category = '이평선'
        st.slider(category, 5, 200, 55, 1, key=category)
        for col, val in zip(st.columns(4), [21, 34, 55, 89]):
            버튼(col, category, val)
    with col3:
        category = 'ATR계수'
        st.slider(category, 0.5, 3.0, 2.0, 0.1, key=category)
        for col, val in zip(st.columns(3), [0.5, 1.0, 2.0]):
            버튼(col, category, val)
    df = 야후파이낸스환율추이_가져오기(
        st.session_state.get('기간'),
        st.session_state.get('이평선'),
        st.session_state.get('ATR계수'))
    fig = px.line(df, title='달러 원화 환율 추이')
    st.plotly_chart(fig)
    col1, col2, col3 = st.columns(3)
    상단 = col1.metric('상단(원)', f'{float(df.iloc[-1]["SMA55_UPPER"]):.2f}')
    하단 = col2.metric('하단(원)', f'{float(df.iloc[-1]["SMA55_LOWER"]):.2f}')
    현재 = col3.metric('현재(원)', f'{float(df.iloc[-1]["Close"]):.2f}')