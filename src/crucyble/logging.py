from datetime import datetime
import logging
from pathlib import Path

class LoggingMeta(type):
    _is_logging = True
    _log_location = Path.home() / ".cache" / "{}.log".format(datetime.now().isoformat())

    def no_log(self):
        self._is_logging = False

    @property
    def is_logging(self):
        return self._is_logging

    @classmethod
    def log_to(cls, log_location: Path):
        cls.log_location = log_location

    @property
    def log_location(self):
        if not self._log_location.parent.exists():
            self._log_location.parent.mkdir(exist_ok=True)
        return self._log_location

    @log_location.setter
    def log_location(self, new_location):
        if not isinstance(new_location, Path):
            raise ValueError("GloVe.log_location must be a valid Path object! Got {} instead.".format(type(new_location)))
        self._log_location = new_location
    
    @property 
    def log_location_char(self):
        return str(self.log_location).encode("utf-8")

def logging_callback(logger, log_path: Path):
    with open(log_path, 'r') as f:
        for line in f:
            line = line.rstrip()
            if line != "":
                logger.info(line)   