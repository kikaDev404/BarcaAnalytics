import logging
from shiny import module, ui, render, reactive
from common import*
import config
from os.path import join
from shinywidgets import output_widget, render_widget
from charts import*
import ba_colors_collection.ba_colors as colors
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
                4, ui.card('Over All Data', ui.output_data_frame('barca_num_of_match_played_overall'), style='height: 400px; overflow-y: auto;')
            ),
            ui.column(
                8, ui.card(output_widget('overall_match_bar_graph'), style='height: 400px;')
            ),
        )
    )

@module.server
def overall_panel_server(input,output,session):
     year_data = reactive.Value()
    
     @output
     @render.data_frame
     def barca_num_of_match_played_overall():
       print(barca_data)
       barca_data['Year'] = barca_data['Date'].dt.year
       temp = barca_data.groupby(['Match Result', 'Season']).size().reset_index(name='Number Of Games')
       print(temp)
       year_data.set(temp) 
       
       return render.DataGrid(temp)

     @render_widget
     def overall_match_bar_graph():
        df = year_data.get()

        fig = plot_bar_graph_stacked(df, x_col= 'Season', y_col='Number Of Games', log=log, color_col='Match Result', color=colors.ba_sequential_color.barca_sequential_default_colors, text_col='Number Of Games')
        fig.update_layout(bargap=0.6)
        return fig

       

log.info('Rendering Overall Panel')