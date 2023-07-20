import disnake
from disnake.ext import commands

import config
import random
import asyncio


class Fun(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    
    @commands.slash_command()
    async def fun(self, inter: disnake.AppCmdInter):
        pass
    
    
    @fun.sub_command()
    async def coinflip(inter: disnake.AppCmdInter):
        
        """Flip a coin"""
        
        embed = disnake.Embed(
            color=config.SUCCESS, 
            title="Coinflip",
            description=f"{inter.author.mention} flipped a coin and got **{random.choice(['heads', 'tails'])}**!"
        )
        
        await inter.send(embed=embed)
        
    
    @fun.sub_command()
    async def roll(inter: disnake.AppCmdInter, sides: int, amount: int = 1):
        
        """
        Roll some dice

        Parameters
        ----------
        sides: The number of sides the dice should have (limit of 100)
        amount: The number of dice to roll (limit of 20)
        """
        
        if sides > 100:
            raise commands.BadArgument("The number of sides must be less than or equal to 100.")
        
        if amount > 20:
            raise commands.BadArgument("The number of dice to roll must be less than or equal to 20.")
        
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
            
             
def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
    print(f"Loaded {__name__}")
