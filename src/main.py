import logging

import disnake
from disnake.ext import commands

import config


logger = logging.getLogger("disnake")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="disnake.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

intents = disnake.Intents.all()

bot = commands.InteractionBot(
    reload=True,
    intents=intents,
    activity=disnake.Game(name="Code"),
    test_guilds=[1120835560773271552]
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | Using disnake {disnake.__version__}")
    print("----------------------------------------------\n")

bot.load_extension("cogs.general")
bot.load_extension("cogs.sudo")

bot.run(config.TOKEN)