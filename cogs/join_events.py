import discord
from datetime import datetime, timedelta
import pytz
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from discord.ext import commands
from asyncio import sleep
import requests




class bemvindo(commands.Cog):
    def __init__(self,bot):
        self.bot = bot



    @commands.Cog.listener()  
    async def on_member_join(self, member):
       if member.bot:
            dev = member.guild.get_role(772972514418753586)
            await member.add_roles(dev)
       if member.guild.id == self.bot.guild and not member.bot:
        canal = self.bot.get_channel(772972557015711744)
        membros = len(member.guild.members)
        texto = "<a:emoji:760195465727180852> | **Membros** : "+str(membros).replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣")
        txt = f"{member} entrou no servidor."
        await canal.edit(topic=texto, reason=txt)
        
        #########################################




        #########################################


        cat = member.created_at.replace(tzinfo=pytz.utc).astimezone(tz=pytz.timezone('America/Sao_Paulo')).strftime('`%d/%m/%Y`')
        dias = (datetime.utcnow() - member.created_at).days
        embed = discord.Embed(color=self.bot.cor, description=f'**{member.mention}(`{member.id}`) entrou no servidor, com a conta criada em {cat}({dias} dias).**')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
        await self.bot.get_channel(773567922526355496).send(embed=embed)
        
        ###################################################################
        
        print(f"{member} entrou ")
        url = requests.get(member.avatar_url_as(format="png"))
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((210, 210));
        bigsize = (avatar.size[0] * 2,  avatar.size[1] * 2)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        saida = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        saida.putalpha(mask)

        fundo = Image.open('cogs/img/bem-vindo.png')
        fonte = ImageFont.truetype('cogs/img/college.ttf',42)
        
        escrever = ImageDraw.Draw(fundo)
        escrever.text(xy=(230,345), text=str(member),fill=(0,0,0),font=fonte)
        fundo.paste(saida, (357, 39), saida)

        fundo.save("cogs/img/welcome.png")   
        canal = self.bot.get_channel(772972552393981972)
        await canal.send(f"Olá {member.mention}, seja bem vindo ao servidor **{self.bot.get_user(self.bot.user.id)}**, leia as <#772972551713587210> para ficar por dentro do servidor.", file=discord.File('cogs/img/welcome.png'))
 


    @commands.Cog.listener()  
    async def on_member_remove(self, member):
       if member.guild.id == self.bot.guild:
        canal = self.bot.get_channel(772972557015711744)
        membros = len(member.guild.members)
        texto = "<a:emoji:760195465727180852> | **Membros** : "+str(membros).replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣")
        txt = f"{member} saiu do servidor."
        await canal.edit(topic=texto, reason=txt)

   
def setup(bot):
    bot.add_cog(bemvindo(bot))
