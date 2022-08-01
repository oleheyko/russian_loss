import streamlit as st
from armyloss import ArmyLoss

s = ArmyLoss()


st.title("Russia's war against Ukraine: Losses since 24 February 2022")

st.subheader("Russia's military losses by days")

options = st.multiselect(
     'Please, choose single or multiple categories to create a line plot:',
     s.get_columns()[:-1])

if options:
    fig = s.get_linechart(options)
    st.pyplot(fig)


st.subheader("Russia's millitary loss per a week")

option = st.selectbox(
     ' Please, select category:',
     ('Aircrafts', 'Helicopters', 'Unmanned Aircrafts', 'Armoured Fighting Vehicles', 'Tanks', 'Artillery', 'Multiple Rocket Launchers', 'Air Defence Systems', 'Manpower'))


if option == 'Aircrafts':
    st.image('./aircrafts.png')
elif option == 'Unmanned Aircrafts':
    st.image('./bpla.png')
elif option == 'Helicopters':
    st.image('./helicopters.png')
elif option == 'Armoured Fighting Vehicles':
    st.image('./bbm.png')
elif option == 'Tanks':
    st.image('./tanks.png')