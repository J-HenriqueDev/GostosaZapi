import random
import time
import discord
import datetime
import aiohttp
import json
import typing
import asyncio
from discord.ext import commands


from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions


# gifs
angry = ["https://media.giphy.com/media/y7Vdxx9BTDbeo/giphy.gif","https://media.giphy.com/media/3o7aD8BYLqkQ4NU9Bm/giphy.gif","https://media.giphy.com/media/vxMptG92TpInm/giphy.gif","https://media.giphy.com/media/viUFlZEhCl8s0/giphy.gif","https://media.giphy.com/media/mXH3XrbRo0TRK/giphy.gif"] #giphy angry links
cave = ["https://media.giphy.com/media/l378ycV5Pt6ysGsTe/giphy.gif","https://media.giphy.com/media/avRrO6UNCUOfm/giphy.gif","https://media.giphy.com/media/y7Vdxx9BTDbeo/giphy.gif"]
slap = ["http://imgur.com/Lv5m6cb.gif", "http://i.imgur.com/BsbFQtz.gif", "http://i.imgur.com/hyygFya.gif", "http://i.imgur.com/XoHjIlP.gif","https://media.giphy.com/media/xmWrQVs98kaaI/giphy.gif","https://media.giphy.com/media/AKvtuMkISxWy4/giphy.gif","https://media.giphy.com/media/GdAmjKhcXWJ6U/giphy.gif","https://media.giphy.com/media/Jp3v0iCuOI3vpCFvf4/giphy.gif"] #giphy slap links
dance = ["https://media.giphy.com/media/LeQ4gz6XOhla8/giphy.gif","https://media.giphy.com/media/k7J8aS3xpmhpK/giphy.gif","https://media.giphy.com/media/gOYbQgE1VflzW/giphy.gif"]
hug = ["https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif?itemid=14246498",
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
                "https://media1.tenor.com/images/11b756289eec236b3cd8522986bc23dd/tenor.gif?itemid=10592083"] #giphy hug links
kiss = ['https://imgur.com/iclUiUN.gif',
  'https://imgur.com/lYQt9rx.gif',
  'https://imgur.com/w1TU5mR.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_male/gif_318.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_female/gif_0.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_359.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_female/gif_296.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_357.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_362.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_female/gif_288.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_391.gif',
  'https://loritta.website/assets/img/actions/kiss/both/gif_281.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_382.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_male/gif_321.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_384.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_358.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_381.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_339.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_375.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_380.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_female/gif_289.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_351.gif',
  'https://loritta.website/assets/img/actions/kiss/both/gif_284.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_366.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_343.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_male/gif_301.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_355.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_male/gif_317.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_367.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_377.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_male/gif_302.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_354.gif',
  'https://loritta.website/assets/img/actions/kiss/both/gif_287.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_387.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_male/gif_300.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_352.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_330.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_363.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_male/gif_325.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_372.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_male/gif_378.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_327.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_female/gif_297.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_female/gif_292.gif',
  'https://loritta.website/assets/img/actions/kiss/male_x_male/gif_320.gif',
  'https://loritta.website/assets/img/actions/kiss/female_x_female/gif_360.gif'] #giphy kiss links
attack = ["https://loritta.website/assets/img/actions/attack/generic/gif_36.gif","https://loritta.website/assets/img/actions/attack/generic/gif_90.gif","https://loritta.website/assets/img/actions/attack/generic/gif_67.gif","https://loritta.website/assets/img/actions/attack/generic/gif_3.gif","https://loritta.website/assets/img/actions/attack/generic/gif_96.gif"] #giphy attack links
omg = ["https://media.giphy.com/media/1FMaabePDEfgk/giphy.gif","https://media.giphy.com/media/y9ZDMJ8wITAg8/giphy.gif","https://media.giphy.com/media/P4133zeloooHm/giphy.gif"] #giphy omg links
rage = ["https://media.giphy.com/media/o7C2BKtp6gSd2/giphy.gif","https://media.giphy.com/media/ef7GqsDYDIKFa/giphy.gif",""] #giphy rage links
end = ["https://media.giphy.com/media/xtYMajJxmaBEc/giphy.gif"] #giphy end links
dead = ["https://media.giphy.com/media/jbYg6rjSO82zu/giphy.gif"] #giphy dead links
alive = ["https://media.giphy.com/media/8nf2FVuSIhSYE/giphy.gif"] #giphy alive links
highfives = ["https://media.giphy.com/media/26ufmAlKt4ne2JDnq/giphy.gif","https://media.giphy.com/media/cxPtMDHG8Ljry/giphy.gif","https://media.giphy.com/media/8MFkW6mDff37G/giphy.gif"] #giphy highfive links

       

class Interação(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.command(name='endeline')
    async def endeline(self, ctx):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        gif = random.choice(end)
        endmessage = '**Sem mais vai e vem!**'
        embed = discord.Embed(title="**FIM DE JOGO!**", colour=discord.Colour(0x370c5e),
                              description="{}".format(endmessage))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        await ctx.send(embed=embed, delete_after=10)

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='emputece', aliases=['angry', 'rage'])
    async def emputece(self, ctx, member: discord.Member, membro=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == membro == member:
                await ctx.invoke(self.bot.get_command('endeline'))
                await msg.delete()

        gif = random.choice(rage)

        emputece2 = '{} **Deixou** {} **PUTO!**'.format(membro.mention, member.mention)
        embed = discord.Embed(title="**EMPUTECEU!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(emputece2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😡')

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "😡"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.bot.get_command('putin'), ctx.author, member)
    



    @commands.guild_only()
    @commands.command(name='putin')
    async def putin(self, ctx, member: discord.Member, membro=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        gif = random.choice(rage)

        emputece1 = '**SAI DA FRENTE QUE AGORA EU TO PUTA CONTIGO!**. \n\nEU VOU MATAR o ' \
                    'usuário {}'.format(ctx.author.mention)
        emputece2 = '{} **Deixou** {} **MAIS PUTO AINDA !**'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**EMPUTECEU MAIS AINDA !**", colour=discord.Colour(0x370c5e),
                                description="{}".format(emputece2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😡')

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "😡"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.bot.get_command('endeline'))

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='bate', aliases=['hit', 'punch'])
    async def bate(self, ctx, member: discord.Member, membro=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.bot.get_command('endeline'))
                await msg.delete()

        """<membro>: Tome cuidado com isso."""
        gif = random.choice(slap)

        bate2 = '{} **deu um tapa em** {}'.format(membro.mention, member.mention)
        embed = discord.Embed(title="**Tapão!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(bate2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.bot.get_command('bate'), ctx.author, member)
            



    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='abraça', aliases=['hug', 'abraço'])
    async def abraça(self, ctx, member: discord.Member, membro=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.bot.get_command('endeline'))
                await msg.delete()

        """<membro>: Use isso com amor <3."""
        gif = random.choice(hug)

        abraça2 = '{} **deu um abraço em** {}'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Abraço!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(abraça2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.bot.get_command('abraça'), ctx.author, member)

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='beija', aliases=['kiss', 'beijou'])
    async def beija(self, ctx, member: discord.Member, membro=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.bot.get_command('endeline'))
                await msg.delete()

        """<membro>: Use isso com amor <3."""
        gif1 = random.choice(slap)
        gif2 = random.choice(kiss)
        beija2 = '{} **deu um beijo em** {}'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Beijo!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(beija2))

        embed.set_image(url="{}".format(gif2))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.bot.get_command('beija'), ctx.author, member)

    @commands.command()
    async def tnc(self, ctx):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        gif1 = random.choice(angry)
        gif2 = random.choice(omg)

        person = random.choice(list(ctx.guild.members))

        tnc1 = '{} mandou {} tomar no cu!'.format(ctx.author.mention, person.mention)

        embed = discord.Embed(title="**Raiva!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(tnc1))
        embed.set_image(url="{}".format(gif2))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😮')
            

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='voltapracaverna', aliases=['caverna', 'goback'])
    async def voltapracaverna(self, ctx, member: discord.Member, membro=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.bot.get_command('endeline'))
                await msg.delete()

        """<membro>: Use isso com amor <3."""
        gif = random.choice(cave)

        cave2 = '{} **mandou** {} **de volta pra caverna**'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Volta pra Caverna!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(cave2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.bot.get_command('voltapracaverna'), ctx.author, member)
    
    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='dança', aliases=['dance', 'dançar'])
    async def dança(self, ctx, member: discord.Member, membro=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.bot.get_command('endeline'))
                await msg.delete()

        """<membro>: Use isso com amor <3."""
        gif = random.choice(dance)

        dança2 = '{} **começou a dançar com** {}'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Dançante!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(dança2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.bot.get_command('dança'), ctx.author, member)

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='ataca', aliases=['attack', 'atacar'])
    async def ataca(self, ctx, member: discord.Member, membro=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.bot.get_command('endeline'))
                #await msg.delete()
        """<membro>: Cuidado com isso!"""
        gif = random.choice(attack)
        ataca2 = '{} **deu um ataque em** {}'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Ataque!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(ataca2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.bot.get_command('ataca'), ctx.author, member)
            

    @commands.guild_only()
    @commands.command(name='roletarussa', aliases=['roleta', 'rr'])
    async def roletarussa(self, ctx):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')
        gif1 = random.choice(dead)
        gif2 = random.choice(alive)

        embed = discord.Embed(
            title=f"*Vamos começar a jogar, {ctx.message.author.name} ? Chame mais pessoas para jogarem conosco!*",
            colour=discord.Colour(0x370c5e))

        embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        embed.add_field(name="**Regras do jogo:**",
                        value="```Clique na arma para participar. Quando tivermos 6 participantes começarei o jogo!```")
        message = await ctx.send(embed=embed)
        await message.add_reaction("🔫")

        def check(reaction, number_of_reactions):
            return reaction.count == 6 and str(reaction.emoji) == '🔫'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)

        except:
            return

        if str(reaction.emoji) == "🔫":

            iterator = reaction.users()
            users = await iterator.flatten()
            while len(users) > 1:
                loser = random.choice(users)
                users.remove(loser)
                msg1 = f'``Que pena, você morreu, {loser}!``'
                embed = discord.Embed(title="**Morte!**", colour=discord.Colour(0x370c5e),
                                        description="{}".format(msg1))
                embed.set_image(url="{}".format(gif1))
                embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

                msg = await ctx.send(embed=embed)
                await asyncio.sleep(5)

            winner = random.choice(users)
            msg2 = f'``Parabéns, {winner}! Você sobreviveu!``'
            embed = discord.Embed(title="**Sobreviveu!**", colour=discord.Colour(0x370c5e),
                                    description="{}".format(msg2))
            embed.set_image(url="{}".format(gif2))
            embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
            msg = await ctx.send(embed=embed)
            
    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='highfive', aliases=['hf', 'batemao'])
    async def highfive(self, ctx, member: discord.Member, membro: discord.Member = None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.bot.get_command('endeline'))
                await msg.delete()
        """<membro>: Cuidado com isso!"""
        gif = random.choice(highfives)
        ataca2 = '{} e {} **Deram um High Five!**'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Shipados!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(ataca2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.bot.get_command('highfive'), ctx.author, member)
            




def setup(bot):
    bot.add_cog(Interação(bot))