import logging
import os
from pathlib import Path


def setup_logging():
    # Define the project root and logs directory
    project_root = Path(__file__).resolve().parents[1]
    logs_dir = project_root / "logs"

    # Create logs directory if it doesn't exist
    if not logs_dir.exists():
        os.makedirs(logs_dir)

    # Log file paths
    test_log_file = logs_dir / "test.log"
    error_log_file = logs_dir / "error.log"

    # Set up main logger (for test.log)
    logger = logging.getLogger("main")
    if not logger.hasHandlers():  # Ensure handlers are only added once
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(test_log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Set up error logger (for error.log)
    error_logger = logging.getLogger("error")
    error_logger.propagate = False  # Prevent logging to the main logger
    if not error_logger.hasHandlers():
        error_handler = logging.FileHandler(error_log_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        error_logger.addHandler(error_handler)

    return logger, error_logger
