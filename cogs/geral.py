import discord
import math
import asyncio
import requests
import time
import datetime
from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from random import choice

class Geral(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Mostra o meu ping', usage='c.ping')
    async def ping(self, ctx):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        embed = discord.Embed(title="🏓 Pong!",
                              description=f' No Momento estou com: **{round(self.bot.latency * 1000)}ms**.',
                              color=0x36393f)
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=90)

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Listagem e informações de todos os comandos públicos lançados até o momento',usage='c.ajuda',aliases=['help'])
    async def ajuda(self, ctx, nome = None):
        incorreto = self.bot._emojis["incorreto"]
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if nome:
            comando = self.bot.get_command(nome)
            if not comando:
                return await ctx.send(f"{incorreto }**{ctx.author.name}**! Não foi possível encontrar um comando chamado **`{nome[:15]}`**.", delete_after=15)

            nome = comando.name
            desc = comando.description
            uso = comando.usage
            if not desc: desc = "Descrição não definida."
            if not uso: uso = "Modo de uso não definido."
            if comando.aliases:
                aliases = ', '.join([f"**`{alias}`**" for alias in comando.aliases])
            else:
                aliases = "Nenhuma abreviação."

            embed = discord.Embed(colour=self.bot.cor)
            embed.set_author(name=f"Informações do comando {nome}.")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
            embed.add_field(name=f"**Uso**",value=f"`{uso}`")
            embed.add_field(name=f"**Abreviações**",value=aliases)
            embed.add_field(name=f"**Descrição**",value=f"`{desc}`")
            return await ctx.send(embed=embed)
    

        em = discord.Embed(colour=self.bot.cor, description="\n**[Prefixos]:** `c.comando`, `C.comando`\n")
        em.set_author(name=f"{self.bot.user.name} | Comandos")
        em.set_thumbnail(url=self.bot.user.avatar_url)
        
        for name, cog in self.bot.cogs.items():
            cmds = [c for c in cog.get_commands() if not c.hidden]
            value = '| '.join([f'`{c}`' for c in cmds])

            if value:
                em.add_field(name=f'**Comandos de {name}**: ({len(cmds)})', value=value, inline=False)
        em.add_field(
            name='\u200b',
            value=f'Digite **{ctx.prefix}{ctx.invoked_with} <Comando>** para ver mais ' \
                'informações sobre um comando.',
            inline=False
        )
        em.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed=em)


    
    @commands.command(description='Mostra a quantidade de invites de um Membro.',usage='c.invites <@Membro>',aliases=["invite","convidados"],hidden=True)
    @commands.bot_has_permissions(embed_links=True)
    async def invites(self, ctx, *, user: str=None):
        if not user:
            user = ctx.author
        elif "<" in user and "@" in user:
            userid = user.replace("@", "").replace("<", "").replace(">", "").replace("!", "")
            user2 = discord.utils.get(ctx.guild.members, id=int(userid))
            if not user2:
                user = discord.utils.get(self.bot.get_all_members(), id=int(userid))
            else:
                user = user2
        elif "#" in user and user[len(user) - 4:].isdigit(): 
            splituser = user.split("#")
            user2 = discord.utils.get(ctx.guild.members, name=splituser[0], discriminator=splituser[1])
            if not user2:
                user = discord.utils.get(self.bot.get_all_members(), name=splituser[0], discriminator=splituser[1])
            else:
                user = user2
        else:
            try:
                int(user)
                user = await self.bot.get_user_info(user)
            except:
                user2 = discord.utils.get(ctx.guild.members, name=user)
                if not user2:
                    user = discord.utils.get(self.bot.get_all_members(), name=user)
                else:
                    user = user2
        if not (isinstance(user, discord.Member) or isinstance(user, discord.User)):
            comma = user.args[0].split('"')[1]
            embed = discord.Embed(title=f"{self.bot._emojis['incorreto']} | Membro não encontrado!", color=self.bot.cor, description=f"O membro `{comma}` não está nesse servidor.")
            embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
            await ctx.send(embed=embed)
            return
        amount = 0
        total = 0
        entries = {}
        for x in await ctx.guild.invites():
            if user == x.inviter:
                amount += x.uses
            total += x.uses
        for x in await ctx.guild.invites():
            if x.uses > 0:
                if "user" not in entries:
                    entries["user"] = {}
                if str(x.inviter.id) not in entries["user"]:
                    entries["user"][str(x.inviter.id)] = {}
                if "uses" not in entries["user"][str(x.inviter.id)]:
                    entries["user"][str(x.inviter.id)]["uses"] = 0
                entries["user"][str(x.inviter.id)]["uses"] += x.uses
        try: 
            entries["user"]
        except:
            return await ctx.send("No-one has made an invite in this server :no_entry:")
        if str(user.id) not in entries["user"]:
            await ctx.send("{} has no invites :no_entry:".format(user))
            return
        sorted_invites = sorted(entries["user"].items(), key=lambda x: x[1]["uses"], reverse=True)
        place = 0
        percent = (amount/total)*100
        if percent < 1:
            percent = "<1"
        else:
            percent = round(percent)
        for x in sorted_invites:
            place += 1
            if x[0] == str(user.id):
                break 
        await ctx.send("{} has **{}** invites which means they have the **{}** most invites. They have invited **{}%** of all users.".format(user, amount, self.prefixfy(place), percent))
        del entries


    @commands.command(description="Mostra todos os emojis deste servidor. ",aliases=["emotes", "emojis", "semotes", "semojis", "serveremojis"],hidden=True,usage="c.emojis")
    @commands.bot_has_permissions(embed_links=True)
    async def serveremotes(self, ctx):
        msg = ""
        for x in ctx.guild.emojis:
            if x.animated:
                msg += "<a:{}:{}> ".format(x.name, x.id)
            else:
                msg += "<:{}:{}> ".format(x.name, x.id)
        if msg == "":
            embed = discord.Embed(title=f"{self.bot._emojis['incorreto']} | Emojis Inexistentes!", color=self.bot.cor, description=f"Este servidor não tem nenhum emoji adicionado.\nuse ``c.addemoji`` para adicionar novos emojis.")
            embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
            await ctx.send(embed=embed)
            return
        else:
            i = 0 
            n = 2000
            for x in range(math.ceil(len(msg)/2000)):
                while msg[n-1:n] != " ":
                    n -= 1
                s=discord.Embed(description=msg[i:n])
                i += n
                n += n
                if i <= 2000:
                    s.set_author(name="{} Emojis".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                await ctx.send(embed=s)


    @commands.command(description='Adiciona um emoji neste servidor a partir de um link, imagem ou outro emoji já criado.',usage='c.addemoji <URL ou Emoji>',hidden=True)
    @commands.bot_has_permissions(embed_links=True)
    @commands.bot_has_permissions(manage_emojis=True)
    async def createemote(self, ctx, emote: str=None):
        if not emote:
            if ctx.message.attachments:
                url = ctx.message.attachments[0].url
                split1 = url.split("/")
                split2 = split1[6].split(".")
                emotename = split2[0].replace("-", "_")
            else:
                await ctx.send("An image, url or emote is a required argument :no_entry:")
                return
        elif "https://" in emote or "http://" in emote:
            url = emote
            if "https://cdn.discordapp.com/attachments/" in url:
                split1 = url.split("/")
                split2 = split1[6].split(".")
                emotename = split2[0].replace("-", "_")
            else:
                await ctx.send("Because you're uploading an image and i'm not able to grab the name, the emote needs a name respond with one below. (Respond Below)")
                try:
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel
                    response = await self.bot.wait_for("message", check=check, timeout=30)
                    emotename = response.content.replace(" ", "_").replace("-", "_")
                except asyncio.TimeoutError:
                    await ctx.send("Timed out :stopwatch:")
                    return
        else:
            try:
                emote1 = self.bot.get_emoji(int(emote))
                if not emote1:
                    request = requests.get("https://cdn.discordapp.com/emojis/" + emote + ".gif")
                    if request.text == "":
                        url = "https://cdn.discordapp.com/emojis/" + emote + ".png"
                    else:
                        url = "https://cdn.discordapp.com/emojis/" + emote + ".gif"
                    await ctx.send("I was unable to find this emote in any servers i am in so please provide a name for it below. (Respond Below)")
                    try:
                        def check(m):
                            return m.author == ctx.author and m.channel == ctx.channel
                        response = await self.bot.wait_for("message", check=check, timeout=30)
                        emotename = response.content.replace(" ", "_").replace("-", "_")
                    except asyncio.TimeoutError:
                        await ctx.send("Timed out :stopwatch:")
                        return
                else:
                    emotename = emote1.name
                    url = emote1.url
            except:
                try:
                    if emote.startswith("<a:"):
                        splitemote = emote.split(":")
                        emotename = splitemote[1]
                        emoteid = str(splitemote[2])[:-1]
                        extend = ".gif"
                    else:
                        splitemote = emote.split(":")
                        emotename = splitemote[1]
                        emoteid = str(splitemote[2])[:-1]
                        extend = ".png"
                except:
                    await ctx.send("Invalid emoji :no_entry:")
                    return
                url = "https://cdn.discordapp.com/emojis/" + emoteid + extend
        image = requests.get(url).content
        try:
            emoji = await ctx.guild.create_custom_emoji(name=emotename, image=image)
        except discord.errors.Forbidden:
            await ctx.send("I do not have the manage emojis permission :no_entry:")
            return
        except discord.errors.HTTPException:
            await ctx.send("I was unable to make the emote this may be because you've hit the emote cap :no_entry:")
            return
        except:
            await ctx.send("Invalid emoji/url (Check if it's been deleted or you've made a typo) :no_entry:")
            return
        await ctx.send("{} has been copied and created".format(emoji))

    @commands.command(description='Mostra a lista dos maiores invitantes do servidor.',usage='c.topinviters',aliases=["ilb", "inviteslb","topinvite"],hidden=True)
    @commands.bot_has_permissions(embed_links=True)
    async def topinviters(self, ctx, page: int=None):
        if not page:
            page = 1
        entries, total = {}, 0
        for x in await ctx.guild.invites():
            if x.uses > 0:
                if "user" not in entries:
                    entries["user"] = {}
                if str(x.inviter.id) not in entries["user"]:
                    entries["user"][str(x.inviter.id)] = {}
                if "uses" not in entries["user"][str(x.inviter.id)]:
                    entries["user"][str(x.inviter.id)]["uses"] = 0
                entries["user"][str(x.inviter.id)]["uses"] += x.uses
                total += x.uses
        try: 
            entries["user"]
        except:
            return await ctx.send("No-one has made an invite in this server :no_entry:")
        if page < 1 or page > math.ceil(len(entries["user"])/10):
            return await ctx.send("Página Inválida")
        sorted_invites = sorted(entries["user"].items(), key=lambda x: x[1]["uses"], reverse=True)
        msg, i, place = "", page*10-10, 0
        for x in sorted_invites:
            if str(ctx.author.id) in map(lambda x: x[0], sorted_invites):
                place += 1
                if x[0] == str(ctx.author.id):
                    break 
            else:
                place = None
        for x in sorted_invites[page*10-10:page*10]:
            i += 1
            percent = (x[1]["uses"]/total)*100
            if percent < 1:
                percent = "<1"
            else:
                percent = round(percent)
            user = discord.utils.get(ctx.guild.members, id=int(x[0]))
            if not user:
                user = "Usuário não encontrado"
            msg += "{}. `{}` - {:,} {} ({}%)\n".format(i, user, x[1]["uses"], "invite" if x[1]["uses"] == 1 else "invites", percent)
        s=discord.Embed(title="TOP Inviters", description=msg, colour=0xed2939)
        s.set_footer(text="{}'s Rank: {} | Página {}/{}".format(ctx.author.name, "#{}".format(place) if place else "Unranked", page, math.ceil(len(entries["user"])/10)), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=s)

        

    @commands.guild_only()
    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.bot_has_permissions(embed_links=True)
    @commands.has_permissions(ban_members=True)
    @commands.command(description='Apaga uma quantidade definida de mensagens de um canal.',usage='c.clear 75',aliases=["purge","limpar"])
    async def clear(self,ctx,* ,num=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        correto = self.bot._emojis['correto']
        incorreto = self.bot._emojis['incorreto']

        numero = int(num)
        if numero>100:
            numb = 100
            await ctx.channel.purge(limit=numb)
            embed=discord.Embed(description=f"{correto} **|** Foram apagadas **{numb}** mensagens.", color=self.bot.cor)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await msg.delete()
        elif numero>0:
            await ctx.channel.purge(limit=numero)
            embed=discord.Embed(description=f"{correto} **|** Foram apagadas **{numero}** mensagens.", color=self.bot.cor)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await msg.delete()
        else:
            embed=discord.Embed(description=f"{incorreto} **|** Insirá um valor válido entre (1 a 100).", color=self.bot.cor)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await msg.delete()
        
    @commands.command(hidden=True)
    async def clean(self,ctx, amount: int): 
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        await ctx.channel.purge(limit=amount)
        f = open('cogs/img/deletedTxts.txt', 'a')
        async for message in ctx.channel.history(limit=amount):
            f.write(message.content)
            f.write('\n')
        f.close()
        await ctx.channel.purge(limit=amount)
        await ctx.send('Done!', delete_after=5)


    def prefixfy(self, input):
        number = str(input)
        num = len(number) - 2
        num2 = len(number) - 1
        if int(number[num:]) < 11 or int(number[num:]) > 13:
            if int(number[num2:]) == 1:
                prefix = "st"
            elif int(number[num2:]) == 2:
                prefix = "nd"
            elif int(number[num2:]) == 3:
                prefix = "rd"
            else:
                prefix = "th"
        else:
            prefix = "th"
        return number + prefix
        


    

def setup(bot):
    bot.add_cog(Geral(bot))
