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
        name=st.selectbox("Choose another Column to compare",param_lst)
        # st.write(len(name))
    if isinstance(select_param,str):
        st.write("please select a column with number values")
    else:
        
        
        st.subheader("Line Chart") 
        st.line_chart(df[select_param])
        st.subheader("Bar Chart") 
        st.bar_chart(df[select_param])
        st.subheader("Area Chart") 
        st.area_chart(df[select_param])
        st.subheader("Altair Chart") 
        st.altair_chart(df[select_param])
        
        n = len(df)
        ymax = max(df[select_param])+5
        ymin = 0
        print(n, ymax, ymin)
        
        for i in range(0, 1):
            df_tmp = df.iloc[i:, :]
            print(df_tmp)
            st.markdown(df_tmp.to_html(), unsafe_allow_html=True)
            time.sleep(2)
            with plot_spot:
                make_chart(df_tmp, select_param, ymin, ymax, name)
            time.sleep(2)