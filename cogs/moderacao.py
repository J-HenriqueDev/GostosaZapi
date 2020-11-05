import discord
from datetime import datetime, timedelta
import pytz
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from discord.ext import commands
from asyncio import sleep
import requests


mutedRole = '</Mutado>' # Put here the name of muted members role
memberRole = '👤┃Membro' # Put here the name of members default role

class moderacao(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    @commands.command(no_pm=True,hidden=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cores(self, ctx):
            color_roles = [
                {
                    "name": "──── Colors ────"
                },
                {
                    "name": "Black",
                    "color": discord.Color(0)
                },
                {
                    "name": "Blue",
                    "color": discord.Color(0x4363D8)
                },
                {
                    "name": "Brown",
                    "color": discord.Color(0x9A6324)
                },
                {
                    "name": "Cyan",
                    "color": discord.Color(0x42D4F4)
                },
                {
                    "name": "Green",
                    "color": discord.Color(0x3CB44B)
                },
                {
                    "name": "Grey",
                    "color": discord.Color(0xA9A994)
                },
                {
                    "name": "Lavender",
                    "color": discord.Color(0xE6BEFF)
                },
                {
                    "name": "Lime",
                    "color": discord.Color(0xBFE743)
                },
                {
                    "name": "Magenta",
                    "color": discord.Color(0xF032E6)
                },
                {
                    "name": "Maroon",
                    "color": discord.Color(0x800014)
                },
                {
                    "name": "Mint",
                    "color": discord.Color(0xAAFFC3)
                },
                {
                    "name": "Navy",
                    "color": discord.Color(0x000075)
                },
                {
                    "name": "Olive",
                    "color": discord.Color(0x808012)
                },
                {
                    "name": "Orange",
                    "color": discord.Color(0xF58231)
                },
                {
                    "name": "Pink",
                    "color": discord.Color(0xF4BCBE)
                },
                {
                    "name": "Purple",
                    "color": discord.Color(0x911EB4)
                },
                {
                    "name": "Red",
                    "color": discord.Color(0xE62345)
                },
                {
                    "name": "Teal",
                    "color": discord.Color(0x469990)
                },
                {
                    "name": "White",
                    "color": discord.Color(0xFFFFFF)
                },
                {
                    "name": "Yellow",
                    "color": discord.Color(0xFFE119)
                },
            ]

            for kwargs in color_roles:
                await ctx.guild.create_role(**kwargs, reason="hehe")

    @commands.command()
    @commands.bot_has_permissions(ban_members = True)
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason: str = 'Motivo não informado.'): # Ban command
        # Discord return
        if members is None:
            e = discord.Embed(description = f'Você não informou o usuário a ser banido, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
            e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
            await ctx.send(embed = e)
            await ctx.message.add_reaction('❌')
        else:
            for member in members:
                await member.ban(reason = reason)
                
                e = discord.Embed(colour = self.bot.cor, timestamp = datetime.utcnow())
                e.add_field(name = ':bust_in_silhouette: Usuário', value = f'{member.mention}')
                e.add_field(name = ':crown: Moderador', value = f'{ctx.author.mention}')
                e.add_field(name = ':grey_question: Motivo', value = f'{reason}')
                e.set_author(name = 'BANIDO', icon_url = member.avatar_url)
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.delete()
                
        
       
    @commands.command()
    @commands.bot_has_permissions(ban_members = True)
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member = None): # Unban command
        # Discord return
        if member is None:
            e = discord.Embed(description = f'Você não informou o usuário a ser desbanido, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
            e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
            await ctx.send(embed = e)
            await ctx.message.add_reaction('❌')
        else:
            try:
                banned_users = await ctx.guild.bans()
                member_name, member_discriminator = member.split('#')


                for ban_entry in banned_users:
                    user = ban_entry.user

                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        await ctx.guild.unban(user)
                        
                        e = discord.Embed(title = 'DESBANIDO', colour = 0x3AFE00, timestamp = datetime.utcnow())
                        e.add_field(name = ':bust_in_silhouette: Usuário', value = f'{member}')
                        e.add_field(name = ':crown: Moderador', value = f'{ctx.author.mention}')
                        e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                        await ctx.send(embed = e)
                        await ctx.message.delete()
            
            except Exception:
                await ctx.message.add_reaction('❌')
                e = discord.Embed(description = f'Não foi possível desbanir "{member}", {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)

    @commands.command()
    @commands.bot_has_permissions(kick_members = True)
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, members: commands.Greedy[discord.Member] = None, *, reason: str = 'Motivo não informado.'): # Kick command
        # Discord return
        if members is None:
            e = discord.Embed(description = f'Você não informou o usuário a ser kickado, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
            e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
            await ctx.send(embed = e)
            await ctx.message.add_reaction('❌')
        else:
            for member in members:
                await member.kick(reason = reason)

                e = discord.Embed(colour = self.bot.cor, timestamp = datetime.utcnow())
                e.add_field(name = ':bust_in_silhouette: Usuário', value = f'{member.mention}')
                e.add_field(name = ':crown: Moderador', value = f'{ctx.author.mention}')
                e.add_field(name = ':grey_question: Motivo', value = f'{reason}')
                e.set_author(name = 'KICKADO', icon_url = member.avatar_url)
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.delete()
                
                memberName = member


    @commands.command()
    @commands.bot_has_permissions(kick_members = True)
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, member: discord.Member = None, *, reason: str = 'Motivo não informado.'): # Mute command
        # Discord return
        if member is None:
            e = discord.Embed(description = f'Você não informou o usuário a ser mutado, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
            e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
            await ctx.send(embed = e)
            await ctx.message.add_reaction('❌')
        else:
            role = discord.utils.get(ctx.guild.roles, name = mutedRole)
            if role in member.roles:
                e = discord.Embed(description = f'O usuário já está mutado, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.add_reaction('❌')
            else:
                muted = discord.utils.get(ctx.guild.roles, name = mutedRole)
                if muted is None:
                    await ctx.guild.create_role()
                default = discord.utils.get(ctx.guild.roles, name = memberRole)
                await member.add_roles(muted)
                await member.remove_roles(default)

                e = discord.Embed(colour = 0xFEA900, timestamp = datetime.utcnow())
                e.add_field(name = ':bust_in_silhouette: Usuário', value = f'{member.mention}')
                e.add_field(name = ':crown: Moderador', value = f'{ctx.author.mention}')
                e.add_field(name = ':grey_question: Motivo', value = f'{reason}')
                e.set_author(name = 'MUTADO', icon_url = member.avatar_url)
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.delete()

                # Console return
                print('\n', f'-'*30)
                print(f'\n[+] A mute command has been called!\n\nLog: Author: {ctx.author}, Target: {member}')

    @commands.command()
    @commands.bot_has_permissions(kick_members = True)
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, member: discord.Member = None):
        # Discord return
        if member is None:
            e = discord.Embed(description = f'Você não informou o usuário a ser desmutado, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
            e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
            await ctx.send(embed = e)
            await ctx.message.add_reaction('❌')
        else:
            role = discord.utils.get(ctx.guild.roles, name = mutedRole)
            if role not in member.roles:
                e = discord.Embed(description = f'O usuário não está mutado, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.add_reaction('❌')
            else:
                muted = discord.utils.get(ctx.guild.roles, name = mutedRole)
                default = discord.utils.get(ctx.guild.roles, name = memberRole)
                await member.add_roles(default)
                await member.remove_roles(muted)

                e = discord.Embed(colour = 0x3AFE00, timestamp = datetime.utcnow())
                e.add_field(name = ':bust_in_silhouette: Usuário', value = f'{member.mention}')
                e.add_field(name = ':crown: Moderador', value = f'{ctx.author.mention}')
                e.set_author(name = 'DESMUTADO', icon_url = member.avatar_url)
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.delete()

                # Console return
                print('\n', f'-'*30)
                print(f'\n[+] A mute command has been called!\n\nLog: Author: {ctx.author}, Target: {member}')


   
def setup(bot):
    bot.add_cog(moderacao(bot))