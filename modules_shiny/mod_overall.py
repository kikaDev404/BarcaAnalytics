import logging
from shiny import module, ui, render, reactive
from common import*
import config
from os.path import join
from shinywidgets import output_widget, render_widget
from charts import*
from pre_process import*

project_root = config.DIR_NAMES.project_root
log_folder = join(project_root, config.DIR_NAMES.log_folder)

log_obj = config_log('mod_overall', join(log_folder, 'mod_overall.log'), logging.INFO)
log = log_obj.get_logger()

log.info('Trying to rend Overall Panel')

@module.ui
def overall_panel():
    return ui.card(
        'An Over view of the Game Barca Played from 2000 to 2025',
        ui.row(
            ui.column(
                2, ui.card('Over All Data', ui.output_data_frame('barca_num_of_match_played_overall'))
            ),
            ui.column(
                10, output_widget('overall_match_bar_graph')
            ),
            width = '5px',
        )
    )

@module.server
def overall_panel_server(input,output,session):
     
     year_data = reactive.Value()
    
     @output
     @render.data_frame
     def barca_num_of_match_played_overall():
       barca_data['Year'] = barca_data['MatchDate'].dt.year
       temp = barca_data.groupby('Year').size().reset_index(name='Number Of Games Played')
       year_data.set(temp)
       
       return render.DataGrid(temp)

     @render_widget
     def overall_match_bar_graph():
        df = year_data.get()

        fig = plot_bar_graph(df, x_col= 'Year', y_col='Number Of Games Played', log=log)
        
        return fig

       

log.info('Rendering Overall Panel')