import plotly.express as px
import pandas as pd
from great_tables import GT, style, loc

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

def make_gt_table(df:pd.DataFrame, log, border_color : str = 'solid', table_align : str = 'center', col_header_color : str = 'black'):
    log.info('Trying to make a GT table')
    try:
        gt_table = (
            GT(df)
            .tab_options(table_body_hlines_style=border_color, table_body_vlines_style=border_color, column_labels_vlines_style=border_color)
            .cols_align(align=table_align, columns=None)
            .tab_style(style=style.text(color=col_header_color, weight='bold'), locations=loc.column_labels())
        )
        log.info('Sucessfully made GT table')
    except Exception as ex:
        log.error(f'Error occured while making a GT table {ex}')

    return gt_table

def add_gt_spanner(gt_obj : GT, lables_col_dict : dict, log,spanner_border_color : str = '#D3D3D3', spanner_text_color : str = 'black'):
    log.info('trying to add GT spanner')
    try:
        for spanner_name in lables_col_dict:
            gt_obj =  (
                gt_obj.tab_spanner(label=spanner_name, columns=lables_col_dict[spanner_name])
            )
        
        spanner_name_list = list(lables_col_dict.keys())

        gt_obj = (
            gt_obj.tab_style(style.borders(sides='all', color=spanner_border_color, style = 'solid'), locations=loc.spanner_labels(ids=spanner_name_list))
            .tab_style(style=style.text(color=spanner_text_color, weight='bold'), locations=loc.spanner_labels(ids=spanner_name_list))
        )

        log.info('Successfully added GT Spanner')
    
    except Exception as ex:
        log.error(f'Error Occured while adding GT spanner: {ex}')

    return gt_obj

def conver_bar_plot_for_valuebox(fig,log):
    log.info('Trying to convert the bar plot for value box plotting')
    try:
        fig.update_layout(
        #height=150,
        margin=dict(t=0, r=0, l=0, b=0),
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(visible=False, showgrid=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        )
        log.info('Sucessfully converted the bargraph to a style for valuebox plotting')
        return fig
    
    except Exception as ex:
        log.error(f'Error occured while converting to the bar graph : {ex}')
