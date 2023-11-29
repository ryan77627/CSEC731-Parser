"""
Logging module for http_server.

Makes output nicer and more configurable
"""
from http_server.logger import data
import time

def get_valid_levels():
    # Simple helper to get log levels defined in data.py as string
    return ",".join(data.VALID_LEVELS.keys())
        
def calc_time():
    return round(time.time() * 1000)

class Logger:
    def __init__(self, level):
        # Given a LEVEL, initialize the logger
        self.start_time = calc_time()
        if level not in data.VALID_LEVELS.keys():
            self.log("ERROR", "Please provide a valid log level")
            quit(1)
        else:
            self.current_logging_levels = {k:v for (k,v) in data.VALID_LEVELS.items() if v[0] <= data.VALID_LEVELS[level][0]}.keys()

    def log(self, level, msg):
        # Determine if we need to print msg
        if level in self.current_logging_levels:
            # Level was in returned dictionary, we are going to print a log msg
            current_time = calc_time() - self.start_time
            print(f"{data.VALID_LEVELS[level][1]}{current_time}|{data.VALID_LEVELS[level][2]}: {msg}")
