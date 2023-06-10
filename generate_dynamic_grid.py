import streamlit as st
from utility import make_chart
import time

def generate_dynamic_grid(df):
    #defining containers
    header = st.container()
    select_param = st.container()
    plot_spot = st.empty()
    
    #title
    with header:
        st.title("Dynamic Dashboard")
    #select parmeter drop down
    with select_param:
        param_lst = list(df.columns)
        select_param = st.selectbox('Select a Column: ',   param_lst)
        # name=st.selectbox("Choose another Column:",param_lst)
        # st.write(len(name))
    if isinstance(select_param,str):
        st.write("please select a column with number values")
    else:
        
        
        st.subheader("Line Chart") 
        st.line_chart(df[select_param], use_container_width=True)
        st.subheader("Bar Chart") 
        st.bar_chart(df[select_param], use_container_width=True)
        st.subheader("Area Chart") 
        st.area_chart(df[select_param], use_container_width=True)
        st.subheader("Altair Chart") 
        st.altair_chart(df[select_param], use_container_width=True)
        
        