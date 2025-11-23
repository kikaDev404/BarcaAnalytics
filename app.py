import logging
from shiny import App, render, ui
from os.path import join, dirname, abspath

import config
from common import *
import pre_process

from modules_shiny.mod_overall import *
from modules_shiny.mod_sidebar import *
from modules_shiny.mod_el_classico import *
from modules_shiny.mod_chat import*

# Set up logging
project_root = dirname(abspath(__file__))
log_folder = join(project_root, config.DIR_NAMES.log_folder)
logger_setup = config_log('app.py', join(log_folder, 'main_app.log'), logging.INFO)
log_app = logger_setup.get_logger()
log_app.info('Starting App UI')

# Define UI
app_ui = ui.page_sidebar(
    side_bar_ui('sidebar'),

    ui.page_navbar(
        ui.nav_panel(
            'Overall',
            overall_panel("Overall")
        ),
        ui.nav_panel(
            'EL - Classico',
            el_classico_ui('el_classico')
        ),
        ui.nav_panel(
            'Chat',
            chat_ui('chat')
        )
    ),
    title="FC Barcelona Analytics"
)

# Define Server
def server(input, output, session):
    filter_state = reactive.Value("Home & Away")
    match_played_place_filter = side_bar_server('sidebar', filter_state)
    overall_panel_server('Overall', match_played_place=filter_state)
    el_classico_server('el_classico',match_played_place = filter_state)
    chat_server('chat' , filter_state)

# Run App
app = App(app_ui, server)
