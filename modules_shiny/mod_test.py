import logging
from shiny import module, ui
from common import*
import config
from os.path import join
from pre_process import*
project_root = config.DIR_NAMES.project_root
log_obj = config_log('mod_test', join(project_root, 'mod_test.log'), logging.INFO)
log = log_obj.get_logger()
log.info('Rendering mod_test')
@module.ui
def test_nav():
    return ui.nav_panel(
            'test',
            'testing'
    )
