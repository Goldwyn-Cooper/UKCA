import streamlit as st
import plotly.express as px
from src.data import 은행고시환율_가져오기, 야후파이낸스환율_가져오기, 야후파이낸스환율추이_가져오기, 구글파이낸스환율_가져오기

def 환율정보():
    with st.container(border=True):
        st.header('ℹ️ 환율 정보')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('고시 환율')
            은행고시환율 = 은행고시환율_가져오기()
            st.metric('환율(원)', 은행고시환율.get('basePrice'))
            dt = 은행고시환율.get('date') + ' ' + 은행고시환율.get('time')
            st.caption(f'업데이트 기준 : {dt}')
        with col2:
            야후파이낸스환율 = 야후파이낸스환율_가져오기()
            st.subheader('야후 파이낸스')
            st.metric('환율(원)', f'{float(야후파이낸스환율.iloc[-1]["Close"]):.2f}')
            st.caption(f'업데이트 기준 : {야후파이낸스환율.index[-1].strftime("%Y-%m-%d %H:%M:%S")}')
        with col3:
            구글파이낸스환율 = 구글파이낸스환율_가져오기()
            st.subheader('구글 파이낸스')
            st.metric('환율(원)', f'{float(구글파이낸스환율.get("price")):.2f}')
            st.caption(f'업데이트 기준 : {구글파이낸스환율.get("date")}')
        if st.button('🔄 데이터 최신화', use_container_width=True):
            st.rerun()

def 환율추이():
    with st.container(border=True):
        st.header('📈 환율 추이')
        col1, col2, col3 = st.columns(3)
        def 버튼작동(key, n):
            st.session_state[key] = n
        버튼 = lambda x, y, z : x.button(f'{z}', on_click=lambda : 버튼작동(y, z), use_container_width=True)
        with col1:
            category = '기간'
            st.slider(category, 50, 500, st.session_state.get(category, 200), 1, key=category)
            options = [50, 100, 200]
            for col, val in zip(st.columns(len(options)), options):
                버튼(col, category, val)
        with col2:
            category = '이평선'
            st.slider(category, 5, 200, st.session_state.get(category, 55), 1, key=category)
            options = [21, 55, 144]
            for col, val in zip(st.columns(len(options)), options):
                버튼(col, category, val)
        with col3:
            category = 'ATR계수'
            st.slider(category, 0.5, 3.0, st.session_state.get(category, 2.0), 0.1, key=category)
            options = [0.5, 1.0, 2.0]
            for col, val in zip(st.columns(len(options)), options):
                버튼(col, category, val)
        df = 야후파이낸스환율추이_가져오기(
            st.session_state.get('기간'),
            st.session_state.get('이평선'),
            st.session_state.get('ATR계수'))
        fig = px.line(df, title='달러 원화 환율 추이')
        st.plotly_chart(fig)
        col1, col2, col3 = st.columns(3)
        SMA = f'SMA{st.session_state.get("이평선")}'
        col1.metric('상단(원)', f'{float(df.iloc[-1][SMA+"_UPPER"]):.2f}')
        col2.metric('하단(원)', f'{float(df.iloc[-1][SMA+"_LOWER"]):.2f}')
        col3.metric('현재(원)', f'{float(df.iloc[-1]["Close"]):.2f}')