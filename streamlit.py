import streamlit as st
from armyloss import ArmyLoss

s = ArmyLoss()


st.title("Russia's war against Ukraine: Loss since 24 February 2022")

st.subheader("Russia's military loss by days")

options = st.multiselect(
     'Please, choose single or multiple categories to create a line plot:',
     s.get_columns()[:-1])

if options:
    fig = s.get_linechart(options)
    st.pyplot(fig)


st.subheader("Russia's millitary loss per a week")

option = st.selectbox(
     'Please, select category:',
     s.get_columns()[:-1])

if option:
    fig = s.get_bar_plot(option)
    st.pyplot(fig)
