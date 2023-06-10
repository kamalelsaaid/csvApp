import streamlit as st

def generate_original(df):
    df = st.data_editor(df, num_rows="dynamic")
            
    st.subheader("Line Chart") 
    st.line_chart(df)
    st.subheader("Bar Chart") 
    st.bar_chart(df)
    st.subheader("Area Chart") 
    st.area_chart(df)
    st.subheader("Altair Chart") 
    st.altair_chart(df)