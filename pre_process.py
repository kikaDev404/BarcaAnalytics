from os.path import join
import pandas as pd
from common import*
import config
import logging
import os
import sys



# Initialize the logger setup
logger_setup = config_log(log_name = 'pre_process',log_file=join(config.DIR_NAMES.log_folder, 'preprocess.log'), log_level=logging.INFO)
log = logger_setup.get_logger()

# Get the logger
try:
    project_root =  os.path.dirname(os.path.abspath(__file__))
    log.info(f"Project Root : {project_root}")
    input_dir = join(project_root, config.DIR_NAMES.input_files)
    log.info(f"Input DIR : {input_dir}")
    barca_data = load_df(join(input_dir, config.FILE_NAMES.base_barca_file), log)
except Exception as ex:
    log.error(f"Error Occured, see the log for details : f{ex}")
    sys.exit(1)


barca_data = convert_to_date(barca_data, ['MatchDate'], log)
barca_data.loc[(barca_data['HomeTeam'] == 'Barcelona') & (barca_data['FTResult'] == 'H'), 'Match Result'] = 'Win'
barca_data.loc[(barca_data['AwayTeam'] == 'Barcelona') & (barca_data['FTResult'] == 'A'), 'Match Result'] = 'Win'
barca_data.loc[barca_data['FTResult'] == 'D', 'Match Result'] = 'Draw'
barca_data.loc[(barca_data['HomeTeam'] == 'Barcelona') & (barca_data['FTResult'] == 'A'), 'Match Result'] = 'Lost'
barca_data.loc[(barca_data['AwayTeam'] == 'Barcelona') & (barca_data['FTResult'] == 'H'), 'Match Result'] = 'Lost'
