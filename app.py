from asyncio.log import logger
from tkinter import PROJECTING
from shiny import App, render, ui
import config
from common import*
import logging
import pandas as pd
import pre_process
from os.path import join,dirname,abspath


from modules_shiny.mod_overall import*
from modules_shiny.mod_sidebar import*

project_root =  dirname(abspath(__file__))
log_folder = join(project_root, config.DIR_NAMES.log_folder)
logger_setup = config_log('app.py',join(log_folder, 'main_app.log'),logging.INFO)
log_app = logger_setup.get_logger()
log_app.info('Starting App UI')



app_ui = ui.page_fluid(
    ui.panel_title("FC Barcelona Analytics"),

    ui.page_sidebar(
        side_bar_ui('sidebar'),

    ui.page_navbar( 
        ui.nav_panel(
            'Overall',
            overall_panel("Overall"),  
        ),
    ),

    ),
)


def server(input, output, session):


    match_played_place_filter = side_bar_server('sidebar')
    overall_panel_server('Overall', match_played_place=match_played_place_filter)
    

    


app = App(app_ui, server)
