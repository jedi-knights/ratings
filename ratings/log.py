import logging
import sys

def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a logger with the specified name, log file, and logging level.

    :param name: The name of the logger.
    :param log_file: The file to which logs should be written.
    :param level: The logging level.
    :return: Configured logger instance.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.INFO)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(logging.ERROR)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    return logger


logger = setup_logger('rating_logger', 'ratings.log')

# Example usage
# logger.info('This is an info message')
# logger.error('This is an error message')
