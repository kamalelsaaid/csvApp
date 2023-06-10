
import matplotlib.pyplot as plt
import streamlit as st
import mpld3
import streamlit.components.v1 as components




def genertate_multi_select(df):
    st.dataframe(df)
    option1=st.multiselect("Choose Row to compare",df)
    st.write(len(option1))
    param_lst = list(df.columns)
    index=st.selectbox("Choose Index to compare",param_lst)
    st.write(len(index))
    height=st.selectbox("Choose Height to compare",param_lst)
    st.write(len(height))

    new_df = df.copy()
    df1 = new_df.set_index(index)
    df1 = df1.loc[option1]  

    # plt.plot([1, 2, 3, 4, 5]) 
    fig,ax=plt.subplots()
    
    plt.bar(x=option1, height=df1[height])
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=600)
    # st.pyplot(fig)