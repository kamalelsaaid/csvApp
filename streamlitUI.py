import pip

from generate_dynamic_grid import generate_dynamic_grid
from generate_multi import genertate_multi_select
pip.main(["install", "openpyxl"])
import pandas as pd
from generate_reports import generate_reports
from original_grid import generate_original
import streamlit as st
from customAgGrid import customAgGrid
from all_grids import one_grid_for_all


def handle_grid(df, original_sheet,agGrid_sheet, generate_profile_report, multi_select, dynamic_grid, one_for_all):
    if agGrid_sheet:
        agGrid = customAgGrid()
        agGrid.load_agGrid_sidebar()
        agGrid.generate_agGrid(df)
        
        
    if generate_profile_report:
        generate_reports(df)
        
    if original_sheet:
        
        generate_original(df)
        
    if one_for_all:
        one_grid_for_all(df)
        
    if dynamic_grid:
        generate_dynamic_grid(df)
        
        
    if multi_select:
        genertate_multi_select(df)

def main():
    #Example controlers
    st.set_page_config(page_title="CSV Reader")
    st.header("Visualize your Sheet...")

    csv = st.file_uploader("Upload your CSV only:", type=["csv"])
    xlsx = st.file_uploader("Upload your xlsx only:", type=["xlsx"])


    st.sidebar.subheader("Sidebar options")
    st.sidebar.subheader("Select Single Mode")
    selection_mode = st.sidebar.radio("Selection Mode",
                        ['Original Grid', 'Custom Grid', 'Dynamic Grid',"One Grid for All", "Multi-Select", 'Generate Report'], index=0)
    original_sheet,agGrid_sheet, generate_profile_report=False,False,False
    multi_select, dynamic_grid, one_for_all = False, False, False
    
    if selection_mode=='Original Grid':
        original_sheet=True
        # original_sheet = st.sidebar.checkbox("Second Sheet Option (Original Streamlit)")
    elif selection_mode=='Custom Grid':
        agGrid_sheet = True
        # agGrid_sheet = st.sidebar.checkbox("First Sheet Option (agGrid)")
    elif selection_mode=='Generate Report':
        generate_profile_report=True
        # generate_profile_report = st.sidebar.checkbox("Generate Profile Report")
    elif selection_mode=="Dynamic Grid":
        dynamic_grid = True
        
    elif selection_mode=="Multi-Select":
        multi_select = True
    elif selection_mode=="One Grid for All":
        one_for_all = True
        
    if xlsx is None and csv is None:
        st.write("Please upload the sheet first...")
        
    elif csv:
        df = pd.read_csv(csv)
        handle_grid(df, original_sheet,agGrid_sheet, generate_profile_report, multi_select, dynamic_grid, one_for_all)
        
    elif xlsx:
        df = pd.read_excel(xlsx)
        handle_grid(df, original_sheet,agGrid_sheet, generate_profile_report, multi_select, dynamic_grid, one_for_all)

if __name__ == "__main__":
    main()
