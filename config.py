from dotenv import load_dotenv
import os

load_dotenv()

DB_ENGINE = os.getenv('DB_ENGINE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_BASE = os.getenv('DB_BASE')

DB_DSN = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_BASE}"

