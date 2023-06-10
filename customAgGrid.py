from distutils import errors
from distutils.log import error
import streamlit as st
import pandas as pd 
import altair as alt

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode, ColumnsAutoSizeMode

class customAgGrid:
    def __init__(self) -> None:
        pass
    def load_agGrid_sidebar(self):
        self.sample_size = st.sidebar.number_input("rows", min_value=10, value=40)
        self.grid_height = st.sidebar.number_input("Grid height", min_value=200, max_value=1500, value=300)

        return_mode = st.sidebar.selectbox("Return Mode", list(DataReturnMode.__members__), index=1)
        self.return_mode_value = DataReturnMode.__members__[return_mode]
        
        columns_size = st.sidebar.selectbox("Column Size Mode", list(ColumnsAutoSizeMode.__members__), index=len(ColumnsAutoSizeMode.__members__)-1)
        self.columns_size_value = ColumnsAutoSizeMode.__members__[columns_size]

        update_mode = st.sidebar.selectbox("Update Mode", list(GridUpdateMode.__members__), index=len(GridUpdateMode.__members__)-1)
        self.update_mode_value = GridUpdateMode.__members__[update_mode]
        
        #features
        self.fit_columns_on_grid_load = st.sidebar.checkbox("Fit Grid with all Columns on Load")
        self.quick_search = st.sidebar.checkbox("enable quick search", value = True)

        self.enable_selection=st.sidebar.checkbox("Enable row selection", value=True)
        if self.enable_selection:
            st.sidebar.subheader("Selection options")
            self.selection_mode = st.sidebar.radio("Selection Mode", ['single','multiple'], index=1)
            
            self.use_checkbox = st.sidebar.checkbox("Use check box for selection", value=True)
            if self.use_checkbox:
                self.groupSelectsChildren = st.sidebar.checkbox("Group checkbox select children", value=True)
                self.groupSelectsFiltered = st.sidebar.checkbox("Group checkbox includes filtered", value=True)

            if ((self.selection_mode == 'multiple') & (not self.use_checkbox)):
                self.rowMultiSelectWithClick = st.sidebar.checkbox("Multiselect with click (instead of holding CTRL)", value=False)
                if not self.rowMultiSelectWithClick:
                    self.suppressRowDeselection = st.sidebar.checkbox("Suppress deselection (while holding CTRL)", value=False)
                else:
                    self.suppressRowDeselection=False
            st.sidebar.text("___")

        self.enable_pagination = st.sidebar.checkbox("Enable pagination", value=False)
        if self.enable_pagination:
            st.sidebar.subheader("Pagination options")
            self.paginationAutoSize = st.sidebar.checkbox("Auto pagination size", value=True)
            if not self.paginationAutoSize:
                self.paginationPageSize = st.sidebar.number_input("Page size", value=5, min_value=0, max_value=self.sample_size)
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

        if self.enable_selection:
            gb.configure_selection(self.selection_mode)
            if self.use_checkbox:
                gb.configure_selection(self.selection_mode, use_checkbox=True, groupSelectsChildren=self.groupSelectsChildren, groupSelectsFiltered=self.groupSelectsFiltered)
            if ((self.selection_mode == 'multiple') & (not self.use_checkbox)):
                gb.configure_selection(self.selection_mode, use_checkbox=False, rowMultiSelectWithClick=self.rowMultiSelectWithClick, suppressRowDeselection=self.suppressRowDeselection)

        if self.enable_pagination:
            if self.paginationAutoSize:
                gb.configure_pagination(paginationAutoPageSize=True)
            else:
                gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=self.paginationPageSize)

        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()

        #Display the grid
        st.header("Streamlit Ag-Grid")

        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            height=self.grid_height, 
            width='100%',
            theme='blue', #Add theme color to the table
            columns_auto_size_mode=self.columns_size_value,
            data_return_mode=self.return_mode_value, 
            update_mode=self.update_mode_value,
            fit_columns_on_grid_load=self.fit_columns_on_grid_load,
            enable_quicksearch=self.quick_search,
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            enable_enterprise_modules=True
            )

        df = grid_response['data']
        selected = grid_response['selected_rows']
        selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')
                
                
        with st.spinner("Displaying results..."):
            #displays the chart
            # chart_data = df.loc[:].assign(source='total')
            # if not selected_df.empty :
            #     selected_data = selected_df.loc[:].assign(source='selection')
            #     chart_data = pd.concat([chart_data, selected_data])

            # # chart_data = pd.melt(chart_data, id_vars=['source'], var_name="item", value_name="quantity")
            # chart_data = pd.melt(chart_data)
            # #st.dataframe(chart_data)
            # chart = alt.Chart(data=chart_data).mark_bar().encode(
            #     x=alt.X("item:O"),
            #     y=alt.Y("sum(quantity):Q", stack=False),
            #     color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
            # )

            if not selected_df.empty :
                st.header("Component Outputs - Altair chart")
            

                st.altair_chart(selected_df, use_container_width=True)

                st.subheader("Line Chart") 
                st.line_chart(selected_df)
                st.subheader("Bar Chart") 
                st.bar_chart(selected_df)
                
                st.subheader("Returned grid data:") 

                st.markdown(grid_response['data'].to_html(), unsafe_allow_html=True)
