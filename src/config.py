import os

from dotenv import load_dotenv

load_dotenv()

# bot token
TOKEN = os.getenv("TOKEN")

# embed colors
SUCCESS = 0x4aaeff
WARNING = 0xffcf4a
ERROR = 0xff4a4a

# api keys
CAT_API_KEY = os.getenv("CAT_API_KEY")
DOG_API_KEY = os.getenv("DOG_API_KEY")