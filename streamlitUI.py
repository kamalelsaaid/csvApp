from typing import Set
import os
import shutil
import pandas as pd
from generate_reports import generate_reports

import streamlit as st
from customAgGrid import customAgGrid


def main():
    agGrid = customAgGrid()
    #Example controlers
    st.set_page_config(page_title="CSV Reader")
    st.header("Ask your CSV...")

    sheet = st.file_uploader("Upload your Sheet:", type=["csv"])


    st.sidebar.subheader("Sidebar options")
    
    # custom sidebars
    
    
    agGrid_sheet = st.sidebar.checkbox("First Sheet Option")
    
    original_sheet = st.sidebar.checkbox("Second Sheet Option")
    
    generate_profile_report = st.sidebar.checkbox("Generate Profile Report")
    
    if agGrid_sheet:
        agGrid.load_agGrid_sidebar()

    if sheet is None:
        st.write("Please upload the sheet first...")
        
    else:
        df = pd.read_csv(sheet)
        
        if agGrid_sheet:
            agGrid.generate_agGrid(df)
            
            
        if generate_profile_report:
            generate_reports(df)
            
        if original_sheet:
            df = st.data_editor(df, num_rows="dynamic")


if __name__ == "__main__":
    main()
