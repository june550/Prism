import os

from dotenv import load_dotenv

# bot token
load_dotenv()
TOKEN = os.getenv("TOKEN")

# embed colors
SUCCESS = 0x4aaeff
WARNING = 0xffcf4a
ERROR = 0xff4a4a