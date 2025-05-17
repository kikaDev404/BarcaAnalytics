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

log_obj = config_log('mod_side_bar', join(log_folder, 'mod_side_bar.log'), logging.INFO)
log = log_obj.get_logger()

log.info('Lodding side bar filters')

@module.ui
def side_bar_ui():
    return ui.sidebar(
        ui.card(
            'Filters',
            ui.input_select('match_played_place', 'Match Played', choices=['Home & Away', 'Home', 'Away'], selected='Home & Away')
        )
    )

log.info('Sidebar loaded')

@module.server
def side_bar_server(input, output,session):

    return input.match_played_place

