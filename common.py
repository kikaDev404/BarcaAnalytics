import pandas as pd
import config

def load_df(filename : str, log):
    try:
        log.info(f"Trying to read data from {filename}")
        df = pd.read_csv(filename)
        log.info('Data Read sucessfully')
        return df
    except Exception as ex:
        log.error(ex)
        
def config_log(log_name, log_file, log_level):
    return config.LoggerSetup(log_name = log_name, log_file=log_file, log_level=log_level)

def convert_to_date(df : pd.DataFrame, date_list : list, log) -> pd.DataFrame:
    try:
        log.info(f"trying to convert the {date_list} to dates")
        for date_col in date_list:
            df[date_col] = pd.to_datetime(df[date_col])
        log.info("done converting to date format")
        return df
    except Exception as ex:
        log.error(ex)
    