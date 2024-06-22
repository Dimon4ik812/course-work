import logging

logger = logging.getLogger('save_to_file')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/save_to_file.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)