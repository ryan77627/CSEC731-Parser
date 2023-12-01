"""
Logging module for http_server.

Makes output nicer and more configurable
"""
from http_server.logger import data
import pathlib
import time

def get_valid_levels():
    # Simple helper to get log levels defined in data.py as string
    return ",".join(data.VALID_LEVELS.keys())
        
def calc_time():
    return round(time.time() * 1000)

class Logger:
    def __init__(self, level, file):
        # Given a LEVEL, initialize the logger
        self.start_time = calc_time()
        self.start_real_time = time.localtime()
        # Ensure we have access to the file and start it
        if file:
            self.canonicalized_path = pathlib.Path(file).resolve()
            try:
                if self.canonicalized_path.exists():
                    # Append to file that exists
                    with open(self.canonicalized_path, "a") as f:
                        f.write(f"----- Logging Started on {self.start_real_time.tm_year}-{self.start_real_time.tm_mon:02d}-{self.start_real_time.tm_mday:02d} {self.start_real_time.tm_hour:02d}:{self.start_real_time.tm_min:02d}:{self.start_real_time.tm_sec:02d} -----\n")
                else:
                    # File doesn't exist
                    with open(self.canonicalized_path, "w") as f:
                        f.write(f"----- Logging Started on {self.start_real_time.tm_year}-{self.start_real_time.tm_mon:02d}-{self.start_real_time.tm_mday:02d} {self.start_real_time.tm_hour:02d}:{self.start_real_time.tm_min:02d}:{self.start_real_time.tm_sec:02d} -----\n")
            except Exception as e:
                # Some error making the log file
                self.log("ERROR", f"Error creating log file: {e}")
                quit(1)
        else:
            self.canonicalized_path = None

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
            if self.canonicalized_path != None:
                # Need to log to a file as well
                with open(self.canonicalized_path, "a") as f:
                    f.write(f"{current_time}|{data.VALID_LEVELS[level][2]}: {msg}\n")
