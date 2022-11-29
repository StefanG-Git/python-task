import logging
from datetime import date

logging.basicConfig(level=logging.INFO)

custom_logger = logging.getLogger(__name__)

today = date.today()
file_name = f"{today}.log"
logs_dir = "log_files/"

file_handler = logging.FileHandler(f"{logs_dir}{file_name}")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

custom_logger.addHandler(file_handler)
