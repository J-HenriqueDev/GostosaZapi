
import discord
from discord.ext import commands
import random
import time
import asyncio
from pymongo import MongoClient
import pymongo
import json


startTime = time.time()
def getUptime():
  return time.time() - startTime  

timetime=dict()


class reptop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.canais = ["570908357032935425","571014988622331905"]
    

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def fix_tophelper(self, ctx):
        mongo = MongoClient(self.bot.database)
        bard = mongo['bard']
        users = bard['users']
        top = users.find().sort('reputação', pymongo.DESCENDING).limit(100)
        for valor in top:
          bard.users.update_one({'_id': str(valor['id'])}, {'$set': {'reputação':int(valor['reputação'])}})
          print(f"Fixado : {str(valor['id'])} - {int(valor['reputação'])}")
   

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command(description="Mostra o dos melhores NewHelper's do servidor",usage='c.tophelper',aliases=['top'])
    async def tophelper(self, ctx):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        mongo = MongoClient(self.bot.database)
        bard = mongo['bard']
        users = bard['users']
        top = users.find().sort('reputação', pymongo.DESCENDING).limit(10)
        valores = {}
        users = {}
        index = 1
        texto = []
        rank = []
        for valor in top:
          count = len(rank)
          simb = "count°"
          numero = f"{count}{simb}"
          simbolo = str(numero).replace("0count°", "🥇 **1°**").replace("1count°","🥈 **2°**").replace("2count°","🥉 **3°**").replace("3count°","🏅 **4°**").replace("4count°","🏅 **5°**").replace("5count°","🏅 **6°**").replace("6count°","🏅 **7°**").replace("7count°","🏅 **8°**").replace("8count°","🏅 **9°**").replace("9count°","🏅 **10°**")
          url = f"{simbolo} : <@{valor['_id']}> - ({valor['reputação']})"
          rank.append(url)
           

        url = "\n".join(rank)
        embed=discord.Embed(description=url, color=self.bot.cor)
        embed.set_author(name="Top rank dos </Helper's>", icon_url=ctx.author.avatar_url_as())
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/519287277499973632/522607596851691524/icons8-leaderboard-100.png")
        embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed=embed)


def setup(bot):
    bard.add_cog(reptop(bot))
