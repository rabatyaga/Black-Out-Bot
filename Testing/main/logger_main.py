import logging
from datetime import datetime

logger = logging.getLogger()
handler = logging.FileHandler('main_logger.txt', encoding="UTF-8")
logger.addHandler(handler)

def send_log(msg):
    time_now = datetime.now()
    logger.warning(f'{time_now}: INFO: {msg}')
