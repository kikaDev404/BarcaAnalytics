import logging
from os.path import dirname,abspath

class LoggerSetup:
    def __init__(self,log_name, log_file='logs/app.log', log_level=logging.DEBUG):
        """
        Initialize the LoggerSetup class.
        
        :param log_file: The log file where messages will be saved (default: 'app.log')
        :param log_level: The minimum log level to capture (default: logging.DEBUG)
        """
        self.log_name = log_name
        self.log_file = log_file
        self.log_level = log_level
        self._setup_logger()

    def _setup_logger(self):
        """
        Set up the logger with both file and stream handlers.
        Avoids using basicConfig to ensure independent loggers.
        """
        # Create a logger object
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(self.log_level)

        # Create a file handler to write logs to a file
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.log_level)

        # Create a stream handler to output logs to the console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.log_level)

        # Create a formatter and set it for both handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # Add both handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        """
        Retrieve the logger instance.
        
        :return: The logger instance
        """
        return self.logger


class DIR_NAMES:
    input_files = 'inputs'
    log_folder = 'logs'
    project_root = dirname(abspath(__file__))

class FILE_NAMES:
    base_barca_file = 'Barcelona.csv'
    season_data_file = [
        'season-2425.csv',
        'season-2324.csv',
        'season-2223.csv',
        'season-2122.csv',
        'season-2021.csv',
        'season-1920.csv'
    ]

class SEASON_DATES:
    season_dates = {
        'Season 19-20' : ('16-08-19' ,  '19-07-20'),
        'Season 20-21' : ('12-09-20' , '23-05-21'),
        'Season 21-22' : ('15-08-21',  '22-05-22'),
        'Season 22-23' : ('12-08-22', '04-06-23'),
        'Season 23-24' : ('11-08-23','26-05-24'),
        'Season 24-25' : ('15-08-24', '25-05-25')
    }

class Match_Outcome_Order:
    match_outcome_order = ['Lost', 'Draw', 'Win']

    