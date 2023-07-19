import disnake
from disnake.ext import commands

import config


class Info(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.slash_command()
    async def ping(self, inter: disnake.AppCmdInter):
        
        """Get the bot's current websocket latency"""
        await inter.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")
    
    
    @commands.slash_command()
    async def info(self, inter: disnake.AppCmdInter):
        pass
    
    
    @info.sub_command()
    async def user(inter: disnake.AppCmdInter, user: disnake.User | disnake.Member = None):
        
        """
        Get info about a user/member

        Parameters
        ----------
        user: User to get info about
        """
        
        if user is None:
            user = inter.author
         
        embed = disnake.Embed(color=config.SUCCESS, title="User Info")
        embed.set_thumbnail(user.avatar or user.default_avatar)
        
        embed.set_author(
            name=user, 
            icon_url=user.avatar 
            or user.default_avatar
        )
        
        embed.add_field(
            name="ID", 
            value=user.id, 
            inline=False
        )
        
        embed.add_field(
            name="Registered", 
            value=disnake.utils.format_dt(user.created_at, style="R"), 
            inline=False
        )
        
        if isinstance(user, disnake.Member):
            embed.add_field(
                name="Joined",
                value=disnake.utils.format_dt(user.joined_at, style="R"),
                inline=False
            )
            
            embed.add_field(
                name="Status",
                value=user.status.name.title(),
                inline=False
            )
            
            roles = user.roles[1:] # exclude @everyone
            
            if roles:
                embed.add_field(
                    name=f"Roles ({len(roles)})",
                    value=", ".join(role.mention for role in roles),
                    inline=False
                )

        await inter.send(embed=embed)


    @info.sub_command()
    async def guild(inter: disnake.AppCmdInter):
        
        """Get info about the current guild"""
        
        guild = inter.guild
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title="Guild Info", 
        )
        
        embed.set_author(name=guild.name, icon_url=guild.icon)
        embed.set_thumbnail(guild.icon)
        
        if guild.banner:
            embed.set_image(guild.banner)
        
        embed.add_field(
            name="ID", 
            value=guild.id, 
            inline=False
        )
        
        embed.add_field(
            name="Owner",
            value=guild.owner.mention,
            inline=False
        )
        
        embed.add_field(
            name="Created",
            value=disnake.utils.format_dt(guild.created_at, style="R"),
            inline=False
        )
        
        embed.add_field(
            name="Members",
            value=guild.member_count,
            inline=False
        )
        
        embed.add_field(
            name="Boost Level",
            value=guild.premium_tier,
            inline=False
        )
            
        await inter.send(embed=embed)


    @info.sub_command(name="bot")
    async def _bot(self, inter: disnake.AppCmdInter):
        
        """Get info about the bot"""
        
        embed = disnake.Embed(
            color=config.SUCCESS,
            title="Bot Info",
            description="A cool bot made by june with ❤️ and [disnake!](https://disnake.dev/)",
        )
        
        bot_avatar = self.bot.user.avatar or self.bot.user.default_avatar
        
        embed.set_author(
            name=self.bot.user.name, 
            icon_url=bot_avatar
        )
        
        embed.add_field(
            name="Owner",
            value=self.bot.owner
        )
        
        embed.add_field(
            name="Created",
            value=disnake.utils.format_dt(self.bot.user.created_at, style="R"),
            inline=False,
        )
        
        embed.add_field(
            name="Guild Count",
            value=len(self.bot.guilds),
            inline=False,
        )
        
        embed.add_field(
            name="Command Count",
            value=len(self.bot.all_slash_commands),
            inline=False,
        )
        
        github_button = disnake.ui.Button(
            style=disnake.ButtonStyle.link,
            label="GitHub",
            url="https://github.com/june550/Prism"
        )
        
        await inter.send(embed=embed, components=[github_button])
        

def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
    print(f"Loaded {__name__}")