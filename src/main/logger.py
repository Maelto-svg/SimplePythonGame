import inspect
import logging
import os
from datetime import datetime


class Logger:
    _instance = None  # Class-level variable to hold the single instance
    _log_dir = None  # Directory where logs will be stored
    _global_log_file = None  # Global log file path

    def __new__(cls, *args, **kwargs):
        """Prevent direct instantiation by users."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger("GameLogger")
            cls._instance.logger.setLevel(logging.DEBUG)
            cls._instance._initialize_log_directory()
            cls._instance._set_global_log_file()
        return cls._instance

    @classmethod
    def _initialize_log_directory(cls):
        """Initialize the log directory based on the current date and time."""
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../logs")
        )
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        cls._log_dir = os.path.join(base_path, current_time)

        # Create the directory if it doesn't exist
        os.makedirs(cls._log_dir, exist_ok=True)

    @classmethod
    def _set_global_log_file(cls):
        """Set up the global log file."""
        cls._global_log_file = os.path.join(cls._log_dir, "global.txt")
        global_handler = logging.FileHandler(cls._global_log_file)
        global_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        cls._instance.logger.addHandler(global_handler)

    def _set_log_file(self, log_file=None):
        """Dynamically set the log file based on the caller's name."""
        if log_file is None:
            # Get the caller's file name
            caller_name = inspect.stack()[3].filename.split(os.sep)[-1].split(".")[0]
            log_file = os.path.join(self._log_dir, f"{caller_name}.txt")

        # Set the file handler for the specific log file
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

        self.logger.handlers = [
            h for h in self.logger.handlers if h.baseFilename == self._global_log_file
        ]
        self.logger.addHandler(file_handler)

    def log(self, level, msg, *args, **kwargs):
        """Log a message dynamically setting the log file each time."""
        self._set_log_file()
        self.logger.log(level, msg, *args, **kwargs)

    @staticmethod
    def get_instance(level=logging.DEBUG, log_file=None):
        """Static method to get the singleton instance with dynamic logging level and file."""
        if Logger._instance is None:
            Logger._instance = Logger()  # This calls __new__ to create the instance

        Logger._instance.logger.setLevel(level)  # Set the log level dynamically
        return Logger._instance

    def info(self, msg, *args, **kwargs):
        return self.log(logging.INFO, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        return self.log(logging.DEBUG, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return self.log(logging.ERROR, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return self.log(logging.WARNING, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        return self.log(logging.CRITICAL, msg, *args, **kwargs)
