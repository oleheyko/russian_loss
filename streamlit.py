import streamlit as st
from armyloss import ArmyLoss

s = ArmyLoss()

if "selected" in st.session_state:
    del st.session_state.selected


st.title("Russia's war against Ukraine: Loss since 24 February 2022")


st.text("")

st.caption('The data source is Minifin acees through the following [link](https://index.minfin.com.ua/en/russian-invading/casualties/)')

st.text("")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
     metric, change = s.get_recent_data("Fighter Aircrafts")
     if not change == 0:
          st.metric(label = "Fighter Aircrafts", value = int(metric), delta = int(change))
     else:
          st.metric(label = "Fighter Aircrafts", value = int(metric))
          
with col2:
     metric, change = s.get_recent_data("Helicopters")
     if not change == 0:
          st.metric(label = "Helicopters", value = metric, delta = change)
     else:
          st.metric(label = "Helicopters", value = metric)

with col3:
     metric, change = s.get_recent_data("Unmanned Aircrafts")
     if not change == 0:
          st.metric(label = "Unmanned Aircrafts", value = metric, delta = change)
     else:
          st.metric(label = "Unmanned Aircrafts", value = metric)

with col4:
     metric, change = s.get_recent_data("Cruise Missiles")
     if not change == 0:
          st.metric(label = "Cruise Missiles", value = metric, delta = change)
     else:
          st.metric(label = "Cruise Missiles", value = metric)
     
with col5:
     if not change == 0:
          metric, change = s.get_recent_data("Air Defence Systems", value = metric, delta = change)
     else:
          st.metric(label = "Air Defence Systems", value = metric)
     
col6, col7, col8, col9, col10 = st.columns(5)
     
with col6:
     metric, change = s.get_recent_data("Tanks")
     if not change == 0:
          st.metric(label = "Tanks", value = metric , delta = change)
     else:
          st.metric(label = "Tanks", value = metric)

with col7:
     metric, change = s.get_recent_data("Armoured Vehicles")
     if not change == 0:
          st.metric(label = "Armoured Vehicles", value = metric , delta = change)
     else:
          st.metric(label = "Armoured Vehicles", value = metric)
     
with col8:
     metric, change = s.get_recent_data("Cars and Tank Cars")
     if not change == 0:
          st.metric(label = "Cars and Tank Cars", value = metric , delta = change)
     else:
          st.metric(label = "Cars and Tank Cars", value = metric)
     
with col9:
     metric, change = s.get_recent_data("Multiple Rocket Launcher")
     if not change == 0:
          st.metric(label = "Multiple Rocket Launcher", value = metric, delta = change)
     else:
          st.metric(label = "Multiple Rocket Launcher", value = metric)
          
with col10:
     metric, change = s.get_recent_data("Artillery")
     if not change == 0:
          st.metric(label = "Artillery", value = metric, delta = change)
     else:
          st.metric(label = "Artillery", value = metric)
     
col11, col12, col13, col14, col15 = st.columns(5)

with col11:
     metric, change = s.get_recent_data("Ships and Boats")
     if not change == 0:
          st.metric(label = "Ships and Boats", value = metric , delta = change)
     else:
          st.metric(label = "Ships and Boats", value = metric)
     
with col12:
     metric, change = s.get_recent_data("Special Equipment")
     if not change == 0:
          st.metric(label = "Special Equipment", value = metric , delta = change)
     else:
          st.metric(label = "Special Equipment", value = metric , delta = change)

with col13:
     metric, change = s.get_recent_data("Manpower")
     if not change == 0:
          st.metric(label = "Manpower", value = metric , delta = change)
     else:
          st.metric(label = "Manpower", value = metric)

st.text("")

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
     (s.get_columns()[:-1]))

if option:
    fig = s.get_bar_plot(option)
    st.pyplot(fig)

st.subheader('Box plot of millitary loss  per a day changing with time')
option_box_plot = st.selectbox(
     'Please, select a category:',
     (s.get_columns()[:-1]))

if option_box_plot:
    fig = s.get_box_plot(option_box_plot)
    st.pyplot(fig)