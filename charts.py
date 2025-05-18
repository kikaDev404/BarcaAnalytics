import plotly.express as px
import pandas as pd

def plot_bar_graph(df : pd.DataFrame, x_col : str, y_col : str, log , color = None):
    log.info('Trying to plot Bargraph using Plotly Express')
    try:
        fig = px.bar(df, x=df[x_col], y=df[y_col], color_discrete_sequence=color, color=color)
        log.info('Sucessfully Plotted Bargraph')
        return fig
    except Exception as ex:
        log.error(f"An Error occured while plotting the bargraph : {ex}")

def plot_bar_graph_stacked(df : pd.DataFrame, x_col : str, y_col : str, log, color_col, text_col,color = None, orientation_type = 'v'):
    log.info('Tying to Plot stacked Bar charts')
    try:
        fig = px.bar(df, x = x_col, y = y_col, color=color_col, barmode='stack', color_discrete_sequence=color, text=text_col, orientation=orientation_type)
        log.info('Sucessfully created the Stacked barchart')
        return fig
    except Exception as ex:
        log.error(f"An Error occured while plotting the graph : {ex}")