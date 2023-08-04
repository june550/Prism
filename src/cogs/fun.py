import asyncio
import random

import disnake
import requests
from disnake.ext import commands
from owoify.owoify import Owoness, owoify

import config

# thank you to these awesome APIs:
# TheCatAPI: https://thecatapi.com/
# TheDogAPI: https://thedogapi.com/
# random-d.uk: https://random-d.uk/
# randomfox.ca: https://randomfox.ca/
# xkcd: https://xkcd.com/

class Fun(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    
    @commands.slash_command()
    async def fun(self, inter: disnake.AppCmdInter):
        pass
    
    
    @fun.sub_command()
    async def coinflip(inter: disnake.AppCmdInter):
        
        """Flip a coin"""
        
        outcome = random.choice(["heads", "tails"])
        
        embed = disnake.Embed(
            color=config.SUCCESS, 
            title="Coinflip",
            description=f"{inter.author.mention} flipped a coin and got **{outcome}**!"
        )
        
        await inter.send(embed=embed)
        
    
    @fun.sub_command()
    async def roll(
        inter: disnake.AppCmdInter, 
        sides: commands.Range[int, 0, 100], 
        amount: commands.Range[int, 0, 20]
    ):
        
        """
        Roll some dice

        Parameters
        ----------
        sides: The number of sides the dice should have (limit of 100)
        amount: The number of dice to roll (limit of 20)
        """
        
        outcome = []
        for i in range(amount):
            outcome.append(random.randint(1, sides))
            
        outcome = ", ".join([str(i) for i in outcome])
        
        if amount == 1:
            msg = f"{inter.author.mention} rolled a d{sides} and got **{outcome}**!"
            
        elif amount > 1:
            msg = f"{inter.author.mention} rolled {amount} d{sides}'s and got **{outcome}**!"
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title="Roll",
            description=msg
        )
        
        await inter.send(embed=embed)
            
    
    @fun.sub_command()
    async def rps(self, inter: disnake.AppCmdInter):
        
        """Play rock, paper, scissors against the bot"""
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title="Rock, Paper, Scissors",
            description=f"{inter.author.mention} choose your option!"
        )
        
        rock = disnake.ui.Button(
            emoji="🪨", 
            style=disnake.ButtonStyle.gray, 
            custom_id="rock"
        )
        
        paper = disnake.ui.Button(
            emoji="📄", 
            style=disnake.ButtonStyle.gray, 
            custom_id="paper"
        )
        
        scissors = disnake.ui.Button(
            emoji="✂️", 
            style=disnake.ButtonStyle.gray, 
            custom_id="scissors"
        )
            
        await inter.response.defer()
        
        msg = await inter.edit_original_response(
            embed=embed, components=[rock, paper, scissors]
        )
        
        check = lambda i: (
            i.user.id == inter.author.id 
            and i.message.id == msg.id
        )
        
        try:
            button_inter: disnake.MessageInteraction = await self.bot.wait_for(
                "button_click", timeout=45, check=check)
            
        except asyncio.TimeoutError:
            embed = disnake.Embed(
                color=config.ERROR,
                title="Timed Out",
                description="You took longer than 45 seconds to respond, so I cancelled the game."
            )
            
            await msg.edit(embed=embed, components=[])
            return
        
        user_choice = button_inter.component.custom_id
        bot_choice = random.choice(["rock", "paper", "scissors"])
            
        if user_choice == bot_choice:
            outcome = f"it's a tie!"
            
        elif user_choice == "rock" and bot_choice == "paper":
            outcome = f"{inter.author.display_name} loses!"
            
        elif user_choice == "paper" and bot_choice == "scissors":
            outcome = f"{inter.author.display_name} loses!"
            
        elif user_choice == "scissors" and bot_choice == "rock":
            outcome = f"{inter.author.display_name} loses!"
            
        else:
            outcome = f"{inter.author.display_name} wins!"
            
        description = (
            f"{inter.author.mention} chose **{user_choice}** "
            f"and I chose **{bot_choice}**, {outcome}"
        )
        
        embed = disnake.Embed(
            title="Rock, Paper, Scissors",
            description=description,
            color=config.SUCCESS
        )
        
        await inter.followup.edit_message(
            msg.id, 
            embed=embed, 
            components=[]
        )
    

    @fun.sub_command()
    async def owoify(
        inter: disnake.AppCmdInter, 
        text: commands.String[str, 0, 1500],
        level: str = commands.Param(choices=["uvu", "uwu", "owo"])
    ):
        
        """
        Owoify ywour text :3

        Parameters
        ----------
        text: The text to owoify
        level: The level of owoification to use
        """
        
        levels = {"uvu": Owoness.Uvu, "uwu": Owoness.Uwu, "owo": Owoness.Owo}
        
        owoified_text = owoify(text, levels[level])
        await inter.send(owoified_text)
    
    
    @fun.sub_command()
    async def clapify(inter: disnake.AppCmdInter, text: commands.String[str, 0, 1500]):
        
        """Add 👏 claps 👏 between 👏 your 👏 words 👏"""
        await inter.send(" 👏 ".join(text.split()))


    @fun.sub_command()
    async def cat(inter: disnake.AppCmdInter):
        
        """Get a random image of a cat"""
  
        resp = requests.get(
            f"https://api.thecatapi.com/v1/images/search/", 
            headers={"x-api-key": config.CAT_API_KEY}
        )
        
        resp.raise_for_status()
        cat_img = resp.json()[0]["url"]
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title=f"Here's a cat for you, {inter.author.display_name}!"
        )
        
        embed.set_image(url=cat_img)
        embed.set_footer(text="Powered by TheCatAPI 🐱")
        await inter.send(embed=embed)
        
        
    @fun.sub_command()
    async def dog(inter: disnake.AppCmdInter):
        
        """Get a random image of a dog"""
        
        resp = requests.get(
            f"https://api.thedogapi.com/v1/images/search/", 
            headers={"x-api-key": config.DOG_API_KEY}
        )
        
        resp.raise_for_status()
        dog_img = resp.json()[0]["url"]
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title=f"Here's a dog for you, {inter.author.display_name}!"
        )
        
        embed.set_image(url=dog_img)
        embed.set_footer(text="Powered by TheDogAPI 🐶")
        await inter.send(embed=embed)
    
    
    @fun.sub_command()
    async def duck(inter: disnake.AppCmdInter):
        
        """Get a random image of a duck"""
        
        resp = requests.get("https://random-d.uk/api/random")
        resp.raise_for_status()
        duck_img = resp.json()["url"]
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title=f"Here's a duck for you, {inter.author.display_name}!"
        )
        
        embed.set_footer(text="Powered by random-d.uk 🦆")
        embed.set_image(url=duck_img)
        await inter.send(embed=embed)
    
    
    @fun.sub_command()
    async def fox(inter: disnake.AppCmdInter):
        
        """Get a random image of a fox"""
        
        resp = requests.get("https://randomfox.ca/floof/")
        resp.raise_for_status()
        fox_img = resp.json()["image"]
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title=f"Here's a fox for you, {inter.author.display_name}!"
        )
        
        embed.set_footer(text="Powered by randomfox.ca 🦊")
        embed.set_image(url=fox_img)
        await inter.send(embed=embed)
    
    
    @fun.sub_command_group()
    async def xkcd(self, inter: disnake.AppCmdInter):
        pass
    
    
    @xkcd.sub_command()
    async def latest(self, inter: disnake.AppCmdInter):
        
        """Get the latest xkcd comic"""
        
        resp = requests.get("https://xkcd.com/info.0.json")
        resp.raise_for_status()
        data = resp.json()

        num = data["num"]
        title = data["title"]
        alt = data["alt"]
        img = data["img"]
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title=title,
            description=alt
        )
        
        embed.set_footer(text=f"xkcd #{num}")
        embed.set_image(img)
        await inter.send(embed=embed)
    
    
    @xkcd.sub_command()
    async def random(self, inter: disnake.AppCmdInter):
        
        """Get a random xkcd comic"""
        
        resp = requests.get("https://xkcd.com/info.0.json")
        resp.raise_for_status()
        total_comics = resp.json()["num"]
        
        random_comic = random.randint(1, total_comics)
        
        resp = requests.get(f"https://xkcd.com/{random_comic}/info.0.json")
        resp.raise_for_status()
        data = resp.json()
        
        num = data["num"]
        title = data["title"]
        alt = data["alt"]
        img = data["img"]
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title=title,
            description=alt
        )
        
        embed.set_footer(text=f"xkcd #{num}")
        embed.set_image(img)
        await inter.send(embed=embed)
        

    @fun.error
    async def fun_error(self, inter: disnake.AppCmdInter, error: commands.CommandError):
        
        if isinstance(error, commands.BadArgument):
            
            embed = disnake.Embed(
                color=config.ERROR,
                title="Error",
                description=error
            )
            
            await inter.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
    print(f"Loaded {__name__}")