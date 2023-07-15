import disnake
from disnake.ext import commands

import config


class General(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @commands.slash_command()
    async def ping(self, inter: disnake.AppCmdInter):
        
        """Get the bot's current websocket latency"""
        await inter.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")
        
    
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


    @commands.slash_command()
    async def info(self, inter: disnake.AppCmdInter):
        pass
    
    
    @info.sub_command()
    async def user(inter: disnake.AppCmdInter, user: disnake.User | disnake.Member = None):
        
        """
        Get info about a user

        Parameters
        ----------
        user: User to get info about
        """
        
        if user is None:
            user = inter.author
         
        embed = disnake.Embed(color=config.SUCCESS, title="User Info")
        embed.set_author(name=user, icon_url=user.avatar or user.default_avatar)
        embed.set_thumbnail(user.avatar or user.default_avatar)
        
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
        
        banner = guild.banner
        
        if banner:
            embed.set_image(banner)
        
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


def setup(bot: commands.Bot):
    bot.add_cog(General(bot))
    print(f"Loaded {__name__}")
