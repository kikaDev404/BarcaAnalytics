import plotly.express as px
import pandas as pd

def plot_bar_graph(df : pd.DataFrame, x_col : str, y_col : str, log):
    log.info('Trying to plot Bargraph using Plotly Express')
    try:
        fig = px.bar(df, x=df[x_col], y=df[y_col])
        log.info('Sucessfully Plotted Bargraph')
        return fig
    except Exception as ex:
        log.error(f"An Error occured while plotting the bargraph : {ex}")