import disnake
import requests
from disnake.ext import commands

import config

# using nekos.best api


class Anime(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    @commands.slash_command()
    async def waifu(self, inter: disnake.AppCmdInter):
        
        """Get a random waifu"""
        
        req = requests.get("https://nekos.best/api/v2/waifu").json()
        
        img = req["results"][0]["url"]
        artist = req["results"][0]["artist_name"]
        artist_url = req["results"][0]["artist_href"]
        source_url = req["results"][0]["source_url"]
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            description=f"[Source]({source_url})"
        )
        
        embed.set_image(url=img)
        embed.set_author(name=f"Artist: {artist}", url=artist_url)
        
        await inter.send(embed=embed)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
def setup(bot: commands.Bot):
    bot.add_cog(Anime(bot))
    print(f"Loaded {__name__}")