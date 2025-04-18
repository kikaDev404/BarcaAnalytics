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