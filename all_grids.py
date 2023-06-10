import streamlit as st
import time
import pandas as pd
import altair as alt

def one_grid_for_all(df):
    #defining containers
    header = st.container()
    selected_param = st.container()
    
    #title
    with header:
        st.title("Dynamic Dashboard")
    st.dataframe(df)
    #select parmeter drop down
    with selected_param:
        param_list = list(df.columns)
        
        index = st.selectbox('Select Index: ',   param_list)
        index2 = st.selectbox('Select another Index: ',   param_list)
        st.subheader("Chart") 
        
        c = alt.Chart(df).mark_circle().encode(
        x=index, y=index2, size=index, color=index, tooltip=index2)
        
        bar = alt.Chart(df).mark_bar().encode(
        x=index, y=index2, size=index, color=index, tooltip=index2)
        
        line = alt.Chart(df).mark_line().encode(
        x=index, y=index2, size=index, color=index, tooltip=index2)

    st.altair_chart(c, use_container_width=True)
    st.altair_chart(bar, use_container_width=True)
    st.altair_chart(line, use_container_width=True)
            
        