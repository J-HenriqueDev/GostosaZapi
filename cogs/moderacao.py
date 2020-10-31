import discord
from datetime import datetime, timedelta
import pytz
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from discord.ext import commands
from asyncio import sleep
import requests




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


   
def setup(bot):
    bot.add_cog(moderacao(bot))