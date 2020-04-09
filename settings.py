import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    CONFIRMATION_TOKEN = os.environ['CONFIRMATION_TOKEN']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    GROUP_ID = os.environ['GROUP_ID']
