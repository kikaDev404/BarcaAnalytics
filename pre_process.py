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

season_df_merged = pd.DataFrame()

# Get the logger
try:
    project_root =  os.path.dirname(os.path.abspath(__file__))
    log.info(f"Project Root : {project_root}")
    input_dir = join(project_root, config.DIR_NAMES.input_files)
    log.info(f"Input DIR : {input_dir}")

    log.info('Combining the season data')

    for season_data in config.FILE_NAMES.season_data_file:
        season_df = load_df(join(input_dir, season_data),log)
        season_df_merged = pd.concat([season_df_merged, season_df])

        log.info(f'Done Combining data from {season_data}')
    
    log.info('Done combining the all season data')
    
    log.info(f'Trying to write the season data to base csv file {config.FILE_NAMES.base_barca_file}')
    season_df_merged = season_df_merged.loc[(season_df_merged['HomeTeam'] == 'Barcelona') | (season_df_merged['AwayTeam'] == 'Barcelona')]
    season_df_merged = convert_to_date(season_df_merged, ['Date'],  to_format='%d/%m/%y',  log = log)
    season_df_merged = season_df_merged.sort_values(by='Date')

    season_df_merged['Season'] = season_df_merged['Date'].apply(map_season)
    season_df_merged.to_csv(join(input_dir, config.FILE_NAMES.base_barca_file))
    log.info(f'Done writing the data to {config.FILE_NAMES.base_barca_file}')

    barca_data = load_df(join(input_dir, config.FILE_NAMES.base_barca_file), log)
except Exception as ex:
    log.error(f"Error Occured, see the log for details : f{ex}")
    sys.exit(1)


barca_data = convert_to_date(barca_data, ['Date'], to_format='%Y-%m-%d', log =log)
barca_data.loc[(barca_data['HomeTeam'] == 'Barcelona') & (barca_data['FTR'] == 'H'), 'Match Result'] = 'Win'
barca_data.loc[(barca_data['AwayTeam'] == 'Barcelona') & (barca_data['FTR'] == 'A'), 'Match Result'] = 'Win'
barca_data.loc[barca_data['FTR'] == 'D', 'Match Result'] = 'Draw'
barca_data.loc[(barca_data['HomeTeam'] == 'Barcelona') & (barca_data['FTR'] == 'A'), 'Match Result'] = 'Lost'
barca_data.loc[(barca_data['AwayTeam'] == 'Barcelona') & (barca_data['FTR'] == 'H'), 'Match Result'] = 'Lost'
