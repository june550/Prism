import disnake
from disnake.ext import commands

import config


class Sudo(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    @commands.slash_command()
    @commands.is_owner()
    async def sudo(self, inter: disnake.AppCmdInter):
        pass
    
    
    @sudo.sub_command()
    async def shutdown(self, inter: disnake.AppCmdInter):
        
        """Shutdown the bot (owner only)"""
        
        embed = disnake.Embed(
            color=config.SUCCESS, 
            title="Shutdown Requested", 
            description="Shutting down... Cya later! 👋"
        )
        
        await inter.send(embed=embed)
        self.bot.close()
    
     
    @sudo.error
    async def sudo_error(self, inter: disnake.AppCmdInter, error: commands.CommandError):
        
        if isinstance(error, commands.NotOwner):
            embed = disnake.Embed(
                color=config.ERROR, 
                title="Error", 
                description=error
            )
            
            await inter.send(embed=embed)
        

def setup(bot: commands.Bot):
    bot.add_cog(Sudo(bot))
    print(f"Loaded {__name__}")