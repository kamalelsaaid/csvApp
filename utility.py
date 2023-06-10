import streamlit as st
import plotly.graph_objects as go


#function to make chart
def make_chart(df, y_col, ymin, ymax, name):
    fig = go.Figure(layout_yaxis_range=[ymin, ymax])
    fig.add_trace(go.Scatter(x=df[name], y=df[y_col],
                             mode='lines+markers'))
    
    fig.update_layout(width=900, height=570, xaxis_title='time',
    yaxis_title=y_col)
    st.write(fig)