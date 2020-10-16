from utils.role import cargos
import discord
#from datetime import datetime, timedelta
from asyncio import sleep
from discord.ext import commands

class reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tempo = 0
        self.cooldown = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(758823253825028167)
        channel = discord.utils.get(guild.channels, id=759814491432550451)
        
        if channel is None:
            return
        if not payload.channel_id == 759814491432550451:
            return
        if payload.channel_id == None:
            return
        if payload.user_id in self.cooldown:
            return

        for cargo in cargos:
            if cargo['emoji'] == str(payload.emoji):
                cargo = guild.get_role(cargo['id'])
                membro = guild.get_member(payload.user_id)
                print(f"member : {membro}")
                if cargo not in membro.roles:
                    await membro.add_roles(cargo, reason=f"[{cargo.name}] Selecionou no canal #info")
                    self.cooldown.append(payload.user_id)
                    await sleep(self.tempo)
                    self.cooldown.remove(payload.user_id)
                break     


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id != 759814491432550451:
            return
        
        if payload.user_id in self.cooldown:
            return

        for cargo in cargos:
            if cargo['emoji'] == str(payload.emoji):
                guild = self.bot.get_guild(payload.guild_id)
                cargo = guild.get_role(cargo['id'])
                membro = guild.get_member(payload.user_id)
                if cargo in membro.roles:
                    await membro.remove_roles(cargo, reason=f"[{cargo.name}] Selecionou no canal #info")
                    self.cooldown.append(payload.user_id)
                    await sleep(self.tempo)
                    self.cooldown.remove(payload.user_id)
                break

    
       
    @commands.command()
    async def raid(self,ctx ,role : discord.Role = None):
        role = discord.utils.get(ctx.guild.roles, name=str(role.name))
        if not role is None:
            for channel in ctx.guild.channels:
                await channel.set_permissions(target=role, manage_channel=False)
                await ctx.send('foi')
def setup(bot):
    bot.add_cog(reaction(bot))
