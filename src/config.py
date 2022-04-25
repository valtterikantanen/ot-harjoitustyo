import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))

DB_NAME = os.getenv("DB_NAME")