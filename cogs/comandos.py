import discord
import asyncio
import requests
import time
import datetime
from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from random import choice

class comandos(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Mostra o meu ping', usage='c.ping')
    async def ping(self, ctx):
        embed = discord.Embed(title="🏓 Pong!",
                              description=f' No Momento estou com: **{round(self.bot.latency * 1000)}ms**.',
                              color=0x36393f)
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=90)


    """
    @commands.command()
    async def spotify(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        act = member.activity
        if act is None or not act.type == discord.ActivityType.listening:
            if member == ctx.author:
                await ctx.send(f'{ctx.author.mention} Você não está ouvindo Spotify.')
            else:
                await ctx.send(f'{ctx.author.mention} Esse usuário não está ouvindo Spotify.')
        else:
            end = act.end - datetime.datetime.utcnow()
            end = str(act.duration - end)[2:7]
            dur = str(act.duration)[2:7]
            act = member.activity
            url = requests.get(act.album_cover_url)
            thumb = Image.open(BytesIO(url.content))
            thumb = thumb.resize((245, 245));
            bigsize = (thumb.size[0] * 3, thumb.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(thumb.size, Image.ANTIALIAS)
            thumb.putalpha(mask)

            output = ImageOps.fit(thumb, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)

            if len(act.title) >= 21:
                titulo = act.title[:22]+"..."
            else:
                titulo = act.title
            if len(act.artist) >= 21:
                cantor = act.artist[:22]+"..."
            else:
                cantor = act.artist
            fundo = Image.open('./files/imagem.png')
            fonte = ImageFont.truetype('./files/Err Hostess.otf', 35)
            escrever = ImageDraw.Draw(fundo)
            escrever.text(xy=(365,150), text=str(titulo),fill=(0,0,0),font=fonte)
            escrever.text(xy=(360,230), text=str(end + ' - ' + dur),fill=(0,0,0),font=fonte)
            escrever.text(xy=(365,315), text=str(cantor),fill=(0,0,0),font=fonte)
            fundo.paste(thumb, (45, 113), thumb)
            fundo.save('./files/imagem1.png')

            print('enviando')
            await ctx.send(file=discord.File('./files/imagem1.png'))
            """
    
    @commands.command(name='hug', aliases=['abraço'])
    async def hug(self, ctx, member : discord.Member, membro = None):
        hug_img = ['http://media1.tenor.com/images/e58eb2794ff1a12315665c28d5bc3f5e/tenor.gif?itemid=10195705',
                    'http://media1.tenor.com/images/949d3eb3f689fea42258a88fa171d4fc/tenor.gif?itemid=4900166',
                    'http://media1.tenor.com/images/11889c4c994c0634cfcedc8adba9dd6c/tenor.gif?itemid=5634578',
                    'http://media1.tenor.com/images/d7529f6003b20f3b21f1c992dffb8617/tenor.gif?itemid=4782499',
                    'https://media1.tenor.com/images/7db5f172665f5a64c1a5ebe0fd4cfec8/tenor.gif?itemid=9200935',
                    'https://media1.tenor.com/images/1069921ddcf38ff722125c8f65401c28/tenor.gif?itemid=11074788',
                    'https://media1.tenor.com/images/3c83525781dc1732171d414077114bc8/tenor.gif?itemid=7830142',
                    'https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif?itemid=14246498',
                    "https://media1.tenor.com/images/4d89d7f963b41a416ec8a55230dab31b/tenor.gif?itemid=5166500",
                    "https://media1.tenor.com/images/b77fd0cfd95f89f967be0a5ebb3b6c6a/tenor.gif?itemid=7864716",
                    "https://media1.tenor.com/images/6db54c4d6dad5f1f2863d878cfb2d8df/tenor.gif?itemid=7324587",
                    "https://media1.tenor.com/images/2e155cdda36fc8f806931cd019e9a518/tenor.gif?itemid=15668356",
                    "https://media1.tenor.com/images/5845f40e535e00e753c7931dd77e4896/tenor.gif?itemid=9920978",
                    "https://media1.tenor.com/images/e58eb2794ff1a12315665c28d5bc3f5e/tenor.gif?itemid=10195705",
                    "https://media1.tenor.com/images/7e30687977c5db417e8424979c0dfa99/tenor.gif?itemid=10522729",
                    "https://media1.tenor.com/images/1069921ddcf38ff722125c8f65401c28/tenor.gif?itemid=11074788",
                    "https://media1.tenor.com/images/506aa95bbb0a71351bcaa753eaa2a45c/tenor.gif?itemid=7552075",
                    "https://media1.tenor.com/images/34a1d8c67e7b373de17bbfa5b8d35fc0/tenor.gif?itemid=8995974",
                    "https://media1.tenor.com/images/18474dc6afa97cef50ad53cf84e37d08/tenor.gif?itemid=12375072",
                    "https://media1.tenor.com/images/7db5f172665f5a64c1a5ebe0fd4cfec8/tenor.gif?itemid=9200935",
                    "https://media1.tenor.com/images/40aed63f5bc795ed7a980d0ad5c387f2/tenor.gif?itemid=11098589",
                    "https://media1.tenor.com/images/460c80d4423b0ba75ed9592b05599592/tenor.gif?itemid=5044460",
                    "https://media1.tenor.com/images/daffa3b7992a08767168614178cce7d6/tenor.gif?itemid=15249774",
                    "https://media1.tenor.com/images/b0de026a12e20137a654b5e2e65e2aed/tenor.gif?itemid=7552093",
                    "https://media1.tenor.com/images/44b4b9d5e6b4d806b6bcde2fd28a75ff/tenor.gif?itemid=9383138",
                    "https://media1.tenor.com/images/af76e9a0652575b414251b6490509a36/tenor.gif?itemid=5640885",
                    "https://media1.tenor.com/images/45b1dd9eaace572a65a305807cfaec9f/tenor.gif?itemid=6238016",
                    "https://media1.tenor.com/images/49a21e182fcdfb3e96cc9d9421f8ee3f/tenor.gif?itemid=3532079",
                    "https://media1.tenor.com/images/d3dca2dec335e5707e668b2f9813fde5/tenor.gif?itemid=12668677",
                    "https://media1.tenor.com/images/54e97e0cdeefea2ee6fb2e76d141f448/tenor.gif?itemid=11378437",
                    "https://media1.tenor.com/images/aeb42019b0409b98aed663f35b613828/tenor.gif?itemid=14108949",
                    "https://media1.tenor.com/images/1d91e026ddbb19e7b00bd06b1032ef69/tenor.gif?itemid=15546819",
                    "https://media1.tenor.com/images/d6510db0a868cfbff697d7279aa89b61/tenor.gif?itemid=10989534",
                    "https://media1.tenor.com/images/112c2abcf585b37e6c6950ebc3ab4168/tenor.gif?itemid=5960669",
                    "https://media1.tenor.com/images/684efd91473dcfab34cb78bf16d211cf/tenor.gif?itemid=14495459",
                    "https://media.giphy.com/media/qscdhWs5o3yb6/giphy.gif",
                    "https://media.giphy.com/media/rSNAVVANV5XhK/giphy.gif",
                    "https://thumbs.gfycat.com/JubilantImaginativeCuttlefish-max-1mb.gif",
                    "https://media.giphy.com/media/svXXBgduBsJ1u/giphy.gif",
                    "https://media.giphy.com/media/C4gbG94zAjyYE/giphy.gif",
                    "https://thumbs.gfycat.com/AffectionateWelldocumentedKitfox-small.gif",
                    "https://i.pinimg.com/originals/02/7e/0a/027e0ab608f8b84a25b2d2b1d223edec.gif",
                    "https://78.media.tumblr.com/f95126745e7f608d3718adae179fad6e/tumblr_o6yw691YXE1vptudso1_500.gif",
                    "https://i.pinimg.com/originals/4b/8f/5c/4b8f5ca7bf41461a19e3b4d1e64c1eb5.gif",
                    "https://media1.tenor.com/images/6ac90d7bd8c1c3c61e6a317e4abf260e/tenor.gif?itemid=12668472",
                    "https://media1.tenor.com/images/11b756289eec236b3cd8522986bc23dd/tenor.gif?itemid=10592083"]
        hug = choice(hug_img)
        embed = self.bot.embed(ctx)
        embed.title = "Abraço"
        embed.description = f"**{member}** Ele(a) recebeu um abraço de **{ctx.author.name}**! Que fofos!"
        embed.set_image(url=hug)

        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔁")

        def check(reaction, user):
            return user == member and str(reaction.emoji)

            

        #def check(reaction, user):
            #return user == member and str(reaction.emoji) == "🔁"

            
        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120.0)

        if reaction.emoji == '🔁':
            Hugh = choice(hug_img)
            embed = self.bot.embed(ctx)
            embed.title = "Abraço"
            embed.description = f"**{ctx.author.name}** Ele(a) recebeu um abraço de **{member.name}**! Que fofos!"
            embed.set_image(url=Hugh)
            ret = await ctx.send(embed=embed)

            await ret.add_reaction("🔁")
        
        def check1(reaction, user):
            return user == ctx.author and str(reaction.emoji)

        reaction, user = await self.bot.wait_for('reaction_add', check=check1, timeout=120.0)

        if reaction.emoji == '🔁':
            await ctx.send(f"poha {ctx.author.mention} já vai abraçar {member.mention} dnv? parte logo pro beijo karai")






    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def clear(self,ctx,* ,num=None):
        correto = self.bot._emojis['correto']
        incorreto = self.bot._emojis['incorreto']
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
            await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
            return

        numero = int(num)
        if numero>100:
            numb = 100
            await ctx.channel.purge(limit=numb)
            embed=discord.Embed(description=f"{correto} **|** Foram apagadas **{numb}** mensagens.", color=0x7BCDE8)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await msg.delete()
        elif numero>0:
            await ctx.channel.purge(limit=numero)
            embed=discord.Embed(description=f"{correto} **|** Foram apagadas **{numero}** mensagens.", color=0x7BCDE8)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await msg.delete()
        else:
            embed=discord.Embed(description=f"{incorreto} **|** Insirá um valor válido entre (1 a 100).", color=0x7BCDE8)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await msg.delete()
        
        


    

def setup(bot):
    bot.add_cog(comandos(bot))
