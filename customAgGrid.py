from distutils import errors
from distutils.log import error
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode, ColumnsAutoSizeMode

class customAgGrid:
    def __init__(self) -> None:
        pass
    def load_agGrid_sidebar(self):
        sample_size = st.sidebar.number_input("rows", min_value=10, value=40)
        grid_height = st.sidebar.number_input("Grid height", min_value=200, max_value=1500, value=300)

        return_mode = st.sidebar.selectbox("Return Mode", list(DataReturnMode.__members__), index=1)
        return_mode_value = DataReturnMode.__members__[return_mode]
        
        columns_size = st.sidebar.selectbox("Column Size Mode", list(ColumnsAutoSizeMode.__members__), index=len(ColumnsAutoSizeMode.__members__)-1)
        columns_size_value = ColumnsAutoSizeMode.__members__[columns_size]

        update_mode = st.sidebar.selectbox("Update Mode", list(GridUpdateMode.__members__), index=len(GridUpdateMode.__members__)-1)
        update_mode_value = GridUpdateMode.__members__[update_mode]
        
        #features
        fit_columns_on_grid_load = st.sidebar.checkbox("Fit Grid with all Columns on Load")
        quick_search = st.sidebar.checkbox("enable quick search", value = True)

        enable_selection=st.sidebar.checkbox("Enable row selection", value=True)
        if enable_selection:
            st.sidebar.subheader("Selection options")
            selection_mode = st.sidebar.radio("Selection Mode", ['single','multiple'], index=1)
            
            use_checkbox = st.sidebar.checkbox("Use check box for selection", value=True)
            if use_checkbox:
                groupSelectsChildren = st.sidebar.checkbox("Group checkbox select children", value=True)
                groupSelectsFiltered = st.sidebar.checkbox("Group checkbox includes filtered", value=True)

            if ((selection_mode == 'multiple') & (not use_checkbox)):
                rowMultiSelectWithClick = st.sidebar.checkbox("Multiselect with click (instead of holding CTRL)", value=False)
                if not rowMultiSelectWithClick:
                    suppressRowDeselection = st.sidebar.checkbox("Suppress deselection (while holding CTRL)", value=False)
                else:
                    suppressRowDeselection=False
            st.sidebar.text("___")

        enable_pagination = st.sidebar.checkbox("Enable pagination", value=False)
        if enable_pagination:
            st.sidebar.subheader("Pagination options")
            paginationAutoSize = st.sidebar.checkbox("Auto pagination size", value=True)
            if not paginationAutoSize:
                paginationPageSize = st.sidebar.number_input("Page size", value=5, min_value=0, max_value=sample_size)
            st.sidebar.text("___")

    def generate_agGrid(self, df):
        #Infer basic colDefs from dataframe types
        gb = GridOptionsBuilder.from_dataframe(df)

        #customize gridOptions
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        # gb.configure_column("date_only", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd', pivot=True)
        
        #configures last row to use custom styles based on cell's value, injecting JsCode on components front end
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.value == 'A') {
                return {
                    'color': 'white',
                    'backgroundColor': 'darkred'
                }
            } else {
                return {
                    'color': 'black',
                    'backgroundColor': 'white'
                }
            }
        };
        """)
        gb.configure_column("group", cellStyle=cellsytle_jscode)

        gb.configure_side_bar()

        if enable_selection:
            gb.configure_selection(selection_mode)
            if use_checkbox:
                gb.configure_selection(selection_mode, use_checkbox=True, groupSelectsChildren=groupSelectsChildren, groupSelectsFiltered=groupSelectsFiltered)
            if ((selection_mode == 'multiple') & (not use_checkbox)):
                gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=rowMultiSelectWithClick, suppressRowDeselection=suppressRowDeselection)

        if enable_pagination:
            if paginationAutoSize:
                gb.configure_pagination(paginationAutoPageSize=True)
            else:
                gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=paginationPageSize)

        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()

        #Display the grid
        st.header("Streamlit Ag-Grid")

        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            height=grid_height, 
            width='100%',
            columns_auto_size_mode=columns_size_value,
            data_return_mode=return_mode_value, 
            update_mode=update_mode_value,
            fit_columns_on_grid_load=fit_columns_on_grid_load,
            enable_quicksearch=quick_search,
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            enable_enterprise_modules=True
            )

        df = grid_response['data']
        selected = grid_response['selected_rows']
        selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')
                
                
        with st.spinner("Displaying results..."):
            #displays the chart
            chart_data = df.loc[:,['apple','banana','chocolate']].assign(source='total')

            if not selected_df.empty :
                selected_data = selected_df.loc[:,['apple','banana','chocolate']].assign(source='selection')
                chart_data = pd.concat([chart_data, selected_data])

            chart_data = pd.melt(chart_data, id_vars=['source'], var_name="item", value_name="quantity")
            #st.dataframe(chart_data)
            chart = alt.Chart(data=chart_data).mark_bar().encode(
                x=alt.X("item:O"),
                y=alt.Y("sum(quantity):Q", stack=False),
                color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
            )

            st.header("Component Outputs - Example chart")
            st.markdown("""
            This chart is built with data returned from the grid. rows that are selected are also identified.
            Experiment selecting rows, group and filtering and check how the chart updates to match.
            """)

            st.altair_chart(chart, use_container_width=True)

            st.subheader("Returned grid data:") 
            #returning as HTML table bc streamlit has issues when rendering dataframes with timedeltas:
            # https://github.com/streamlit/streamlit/issues/3781
            st.markdown(grid_response['data'].to_html(), unsafe_allow_html=True)

            st.subheader("grid selection:")
            st.write(grid_response['selected_rows'])