import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
import streamlit as st

def generate_reports(df):
    with st.spinner("Generating reports..."):
        pr = df.profile_report()

    st_profile_report(pr)