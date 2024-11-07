import logging
import os
from pathlib import Path


def setup_logging():
    # Define the project root and logs directory
    project_root = Path(__file__).resolve().parents[1]
    print(f"Project root: {project_root}")
    logs_dir = project_root / "logs"
    # Create logs directory if it doesn't exist
    if not logs_dir.exists():
        os.makedirs(logs_dir)
        print(f"Logs directory created at: {logs_dir}")

    # Log file paths
    test_log_file = logs_dir / "test.log"
    error_log_file = logs_dir / "error.log"

    # Set up main logger to log to file only (no console output)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create file handler for general logs
    file_handler = logging.FileHandler(test_log_file)
    file_handler.setLevel(logging.INFO)

    # Set formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add file handler to logger
    logger.addHandler(file_handler)

    # Create a separate error logger
    error_logger = logging.getLogger('error')
    error_handler = logging.FileHandler(error_log_file)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Add file handler to the error logger
    error_logger.addHandler(error_handler)

    print(f"Logs will be stored in: {test_log_file} and errors in {error_log_file}")

    return logger, error_logger
