import disnake
from disnake.ext import commands

import config


class Avatar(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    @commands.slash_command()
    async def avatar(self, inter: disnake.AppCmdInter):
        pass
    

    @avatar.sub_command()
    async def user(inter: disnake.AppCmdInter, user: disnake.User | disnake.Member = None):
        
        """
        Get a user's avatar

        Parameters
        ----------
        user: User to get the avatar of
        """
        
        if user is None:
            user = inter.author
        
        embed = disnake.Embed(
            color=config.SUCCESS, 
            title=f"Avatar for {user}",
        )
        
        download_button = disnake.ui.Button(
            style=disnake.ButtonStyle.link, 
            label="Download", 
            url=user.avatar.url or user.default_avatar.url
        )
        
        embed.set_image(user.avatar or user.default_avatar)
        await inter.send(embed=embed, components=[download_button])
        
    
    @avatar.sub_command()
    async def guild(inter: disnake.AppCmdInter, member: disnake.Member = None):
        
        """
        Get a member's guild avatar (if set)

        Parameters
        ----------
        member: Member to get the guild avatar of
        """
        
        if member is None:
            member = inter.author
        
        if not isinstance(member, disnake.Member):
            raise commands.MemberNotFound(member)
        
        if not member.guild_avatar:
            raise commands.BadArgument(f"{member.mention} does not have a guild avatar set.")
        
        guild_avatar = member.guild_avatar
        
        embed = disnake.Embed(
            color=config.SUCCESS, 
            title=f"Guild avatar for {member}", 
        )
        
        download_button = disnake.ui.Button(
            style=disnake.ButtonStyle.link, 
            label="Download", 
            url=guild_avatar.url
        )
        
        embed.set_image(guild_avatar.url)
        await inter.send(embed=embed, components=[download_button])
            

    @avatar.error
    async def avatar_error(self, inter: disnake.AppCmdInter, error: commands.CommandError):
        
        if isinstance(error, (commands.MemberNotFound, commands.BadArgument)):
            
            embed = disnake.Embed(
                color=config.ERROR, 
                title="Error", 
                description=error
            )
            
            await inter.send(embed=embed, ephemeral=True)

      
def setup(bot: commands.Bot):
    bot.add_cog(Avatar(bot))
    print(f"Loaded {__name__}")