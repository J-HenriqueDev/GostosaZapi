
import discord
from discord.ext import commands
import random
import time
import asyncio
from pymongo import MongoClient
import pymongo
import json
from datetime import datetime, timedelta


prefixos = ["c.","!","@","/"]
python = ['python', 'py']
javascript = ['javascript','js']
kotlin = ['kotlin','kt']
java = ['java']
ruby = ['ruby','rb']
go = ['golang', 'go']
linguagem = ["python","javascript","java","kotlin","golang","ruby","nenhuma"]
blocklist = []




class helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forms = []

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='envia o formulário de Helper para você',usage='c.helper',aliases=['newhelper'])
    async def helper(self,ctx):   
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis['incorreto'].replace("<"," ").replace(">"," "))
          return
        '''
        dias_servidor = (datetime.utcnow() - ctx.author.joined_at).days
        if dias_servidor < 5:
            embed = discord.Embed(colour=self.bot.cor)
            embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, para você se tornar um `</Helper>` você precisa ter mais de 5 dias no servidor.", color=self.bot.cor)
            return await ctx.send(embed=embed)
        '''
        server = self.bot.get_guild(self.bot.guild)
        newhelper = discord.utils.get(server.roles, name="</Helper>")
        if newhelper in ctx.author.roles:
            return await ctx.send(f'{ctx.author.mention} você já têm o cargo **</Helper>**.',delete_after=30)

        if ctx.author.id in self.forms:
            return await ctx.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, já tem um formulário em aberto no seu DM.", delete_after=30)

        try:
         try:
           self.forms.append(ctx.author.id)
           embed=discord.Embed(description=f":envelope_with_arrow: **|** Olá **{ctx.author.name}**, verifique sua mensagens diretas (DM).", color=self.bot.cor)
           msg = await ctx.send(embed=embed)
           txs = f"  **|** Então você quer ser um **</Helper>** em nosso servidor?\nPara isso precisamos que você preencha um pequeno formulário para cadastramento de seu dados em nosso sistema.\n\n{self.bot._emojis['nome']} **|** Diga-nos seu **Nome completo**: \n{self.bot._emojis['timer']} **|** **2 minutos**"
           embed=discord.Embed(description=txs, color=self.bot.cor)
           msg = await ctx.author.send(embed=embed)

 
           def pred(m):
               return m.author == ctx.author and m.guild is None

           nome = await self.bot.wait_for('message', check=pred, timeout=120.0) 
           if len(nome.content) >=40:              
              await msg.delete()
              embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, o **Nome** que você inseriu passou do limite de 40 caracteres.", color=self.bot.cor)
              self.forms.remove(ctx.author.id)
              msg = await ctx.author.send(embed=embed)
              await asyncio.sleep(30)
              await msg.delete()
           else:
             await msg.delete()
             texto = f"  **|** Agora diga-me sua idade (10 anos a 99 anos)\n{self.bot._emojis['timer']} **|** **2 minutos**"
             embed=discord.Embed(description=texto, color=self.bot.cor)
             msg = await ctx.author.send(embed=embed)
             idade = await self.bot.wait_for('message', check=pred, timeout=120.0) 
             if idade.content.isnumeric() == False:
                await msg.delete()
                embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, a idade que você inseriu não é válida.", color=self.bot.cor)
                self.forms.remove(ctx.author.id)
                msg = await ctx.author.send(embed=embed)
                await asyncio.sleep(30)
                await msg.delete()
             else:
               if len(idade.content) >=3:              
                  await msg.delete()
                  embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, a idade que você inseriu não é válida. (10 anos a 99 anos.)", color=self.bot.cor)
                  self.forms.remove(ctx.author.id)
                  msg = await ctx.author.send(embed=embed)
                  await asyncio.sleep(30)
                  await msg.delete()
               else:
                 await msg.delete()
                 lang = ", ".join(linguagem)
                 langg = str(lang).replace("nenhuma","")
                 texto = f"  **|** Diga-nos a linguagem que você programa. (**Primária**)\nLinguagens : {langg}\n{self.bot._emojis['timer']} **|** **2 minutos**"
                 embed=discord.Embed(description=texto, color=self.bot.cor)
                 msg = await ctx.author.send(embed=embed)
                 lang1 = await self.bot.wait_for('message', check=pred, timeout=120.0) 
                 if not str(lang1.content.lower()) in linguagem:                      
                    await msg.delete()
                    embed = discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, a linguagem que você forneceu é invalida e por isso ação foi cancelada.", color=self.bot.cor)
                    self.forms.remove(ctx.author.id)
                    msg = await ctx.author.send(embed=embed)
                    await asyncio.sleep(30)
                    await msg.delete()
                 elif str(lang1.content.lower()) in linguagem:                      
                   lang = ", ".join(linguagem)
                   await msg.delete()
                   texto = f"  **|** Diga-nos a linguagem que você programa. (**Secundária**)\n(Caso não tenha nenhuma digite **nenhuma**)\nLinguagens : {langg}\n{self.bot._emojis['timer']} **|** **2 minutos**"
                   embed=discord.Embed(description=texto, color=self.bot.cor)
                   msg = await ctx.author.send(embed=embed)
                   lang2 = await self.bot.wait_for('message', check=pred, timeout=120.0) 
                   if not str(lang2.content.lower()) in linguagem:                      
                      await msg.delete()
                      embed = discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, a linguagem que você forneceu é invalida e por isso ação foi cancelada.", color=self.bot.cor)
                      self.forms.remove(ctx.author.id)
                      msg = await ctx.author.send(embed=embed)
                      await asyncio.sleep(30)
                      await msg.delete()
                   elif str(lang2.content.lower()) in linguagem:
                    if str(lang2.content.lower()) == str(lang1.content.lower()): 
                      await msg.delete()
                      embed = discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, a linguagem (**Secundária**) que você forneceu é igual a (**Primária**) e por isso a ação foi cancelada.", color=self.bot.cor)
                      self.forms.remove(ctx.author.id)
                      msg = await ctx.author.send(embed=embed)
                      await asyncio.sleep(30)
                      await msg.delete()
                    else:
                     await msg.delete()
                     texto = f"  **|** Diga-nos por qual motivo quer se tornar um **</Helper>**? (**Motivo** : 20 caracteres no mínimo)\n{self.bot._emojis['timer']} **|** **2 minutos**"
                     embed=discord.Embed(description=texto, color=self.bot.cor)
                     msg = await ctx.author.send(embed=embed)
                     motivo = await self.bot.wait_for('message', check=pred, timeout=120.0)
                     if len(motivo.content) <= 20:
                        await msg.delete()
                        embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, o motivo é muito pequeno. (20 caracteres no mínimo)", color=self.bot.cor)
                        self.forms.remove(ctx.author.id)
                        msg = await ctx.author.send(embed=embed)
                        await asyncio.sleep(30)
                        await msg.delete()
                     else:
                       await msg.delete()
                       embed=discord.Embed(description=f"  **|** Olá **{ctx.author.name}**, abaixo está localizado as informações do seu cadastro caso tenha alguma coisa errada clique na reação ({self.bot._emojis['incorreto']}) para recusar e deletar, caso esteja certo clique na reação ({self.bot._emojis['correto']}).", color=self.bot.cor)
                       embed.set_author(name="SOLICITAÇÂO DE </HELPER>", icon_url=ctx.author.avatar_url_as())
                       embed.add_field(name=f"{self.bot._emojis['nome']} Nome", value = "``"+str(nome.content)+"``", inline=True)
                       embed.add_field(name=f"{self.bot._emojis['ip']} Idade", value = "``"+str(idade.content)+"``", inline=True)
                       embed.add_field(name=f"{self.bot._emojis['api']} Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                       embed.add_field(name=f"{self.bot._emojis['api']} Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                       embed.add_field(name=f":bell: Motivo", value = "``"+str(motivo.content)+"``", inline=True)
                       msg = await ctx.author.send(embed=embed)
                       reactions = [":errado:761205727841746954", ':correto:761205727670829058>']
                       user = ctx.message.author
                       if user == ctx.message.author:
                        for reaction in reactions:
                            await msg.add_reaction(reaction)
                       def check(reaction, user):
                            return user == ctx.message.author and str(reaction.emoji)

                       reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120.0)
                       if reaction.emoji.name == 'errado':
                          await msg.delete()
                          embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** A solicitação de cadastramento foi cancelada.", color=self.bot.cor)
                          self.forms.remove(ctx.author.id)
                          msg = await ctx.author.send(embed=embed)
                          await asyncio.sleep(30)
                          await msg.delete()
                       if reaction.emoji.name == 'correto':
                           self.forms.remove(ctx.author.id)
                           await msg.delete()
                           embed=discord.Embed(color=self.bot.cor)
                           embed.set_author(name="SOLICITAÇÂO DE </HELPER>", icon_url=ctx.author.avatar_url_as())
                           embed.add_field(name="Membro", value="``"+str(ctx.author)+"``", inline=True)
                           embed.add_field(name=f"{self.bot._emojis['nome']} Nome", value = "``"+str(nome.content)+"``", inline=True)
                           embed.add_field(name=f"{self.bot._emojis['ip']} Idade", value = "``"+str(idade.content)+"``", inline=True)
                           embed.add_field(name=f"{self.bot._emojis['api']} Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                           embed.add_field(name=f"{self.bot._emojis['api']} Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                           embed.add_field(name=":bell: Motivo", value = "``"+str(motivo.content)+"``", inline=True)
                           #servidor
                           server = self.bot.get_guild(self.bot.guild)
                           #canal solicitação
                           channel = discord.utils.get(server.channels, id=self.bot.helper)
                           msg = await channel.send(embed=embed, content="@here")
                           user = ctx.message.author
                           if user == ctx.message.author:
                            for reaction in reactions:
                                await msg.add_reaction(reaction)
                           
                           def check8(reaction, user):
                              return user.id != 760196609161822219 and reaction.message.id == msg.id


                           reaction, author = await self.bot.wait_for('reaction_add', check=check8)
                           if reaction.emoji.name == 'correto':
                              await msg.delete()
                              embed = discord.Embed(color=self.bot.cor)
                              embed.set_author(name="</HELPER> ACEITO", icon_url=ctx.author.avatar_url_as())
                              embed.add_field(name=f"{self.bot._emojis['nome']} Helper", value ="``"+str(ctx.author)+"`` (<@"+str(ctx.author.id)+">)", inline=True)
                              embed.add_field(name=f"{self.bot._emojis['ip']} ID", value ="``"+str(ctx.author.id)+"``", inline=True)
                              embed.add_field(name=f"{self.bot._emojis['api']} Linguagem (Prímaria)", value = "``"+str(lang1.content)+"``", inline=True)
                              embed.add_field(name=f"{self.bot._emojis['api']} Linguagem (Secundária)", value = "``"+str(lang2.content)+"``", inline=True)
                              embed.add_field(name=f"{self.bot._emojis['mention']} Aceito por", value = f"<@{author.id}>", inline=True)
                              embed.set_thumbnail(url=ctx.author.avatar_url_as())
                              embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
                              server = self.bot.get_guild(self.bot.guild)
                              channel = discord.utils.get(server.channels, id=self.bot.helper)
                              await channel.send(embed=embed)
                              mongo = MongoClient(self.bot.database)
                              bard = mongo['bard']
                              users = bard['users']
                              users = bard.users.find_one({"_id": str(ctx.author.id)})
                              if users is None:
                                 print("[Helper] : inserido")
                                 serv ={"_id": str(ctx.author.id),"nome": str(nome.content),"id": str(ctx.author.id),"foi_mute":"Não","vezes_mute":"0","linguagem": str(lang1.content) ,"reputação":int(0),"linguagem2": str(lang2.content),"aceito_por":str(author.id)}
                                 bard.users.insert_one(serv).inserted_id
                                 server = self.bot.get_guild(self.bot.guild)
                                 cargo = discord.utils.get(server.roles, name="</Helper>")
                                 await ctx.author.add_roles(cargo)
                                 if lang1.content.lower() in python:
                                   cargo = discord.utils.get(server.roles, name="</Helper Python>")
                                   await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in javascript:
                                    cargo = discord.utils.get(server.roles, name="</Helper JavaScript>")
                                    await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in kotlin:
                                     cargo = discord.utils.get(server.roles, name="</Helper Kotlin>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in java:
                                     cargo = discord.utils.get(server.roles, name="</Helper Java>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in ruby:
                                     cargo = discord.utils.get(server.roles, name="</Helper Ruby>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in go:
                                     cargo = discord.utils.get(server.roles, name="</Helper Golang>")
                                     await ctx.author.add_roles(cargo)
                                 if lang2.content.lower() in python:
                                   cargo = discord.utils.get(server.roles, name="</Helper Python>")
                                   await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in javascript:
                                    cargo = discord.utils.get(server.roles, name="</Helper JavaScript>")
                                    await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in kotlin:
                                     cargo = discord.utils.get(server.roles, name="</Helper Kotlin>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in java:
                                     cargo = discord.utils.get(server.roles, name="</Helper Java>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in ruby:
                                     cargo = discord.utils.get(server.roles, name="</Helper Ruby>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in go:
                                     cargo = discord.utils.get(server.roles, name="</Helper Golang>")
                              else:
                                 print("[Helper] : updatado")
                                 #bard.users.update_many({"_id": str(ctx.author.id)}, {'$set': {"nome": str(nome.content),"id": str(ctx.author.id),"foi_mute":"Não","vezes_mute":"0","foi_devhelper":"Não","vezes_reportado":"0","reputação":int(0),"level":"0","exp":"0","aceito_por":str(author.id)}})
                                 bard.users.update_many({"_id": str(ctx.author.id)}, {'$set': {"nome": str(nome.content),"id": str(ctx.author.id),"foi_mute":"Não","vezes_mute":"0","linguagem": str(lang1.content) ,"reputação":int(0),"linguagem2": str(lang2.content),"aceito_por":str(author.id)}})
                                 server = self.bot.get_guild(self.bot.guild)
                                 cargo = discord.utils.get(server.roles, name="</Helper>")
                                 await ctx.author.add_roles(cargo)
                                 cargo = discord.utils.get(server.roles, name="</Helper>")
                                 await ctx.author.add_roles(cargo)
                                 if lang1.content.lower() in python:
                                   cargo = discord.utils.get(server.roles, name="</Helper Python>")
                                   await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in javascript:
                                    cargo = discord.utils.get(server.roles, name="</Helper JavaScript>")
                                    await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in kotlin:
                                     cargo = discord.utils.get(server.roles, name="</Helper Kotlin>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in java:
                                     cargo = discord.utils.get(server.roles, name="</Helper Java>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in ruby:
                                     cargo = discord.utils.get(server.roles, name="</Helper Ruby>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang1.content.lower() in go:
                                     cargo = discord.utils.get(server.roles, name="</Helper Golang>")
                                     await ctx.author.add_roles(cargo)
                                 if lang2.content.lower() in python:
                                   cargo = discord.utils.get(server.roles, name="</Helper Python>")
                                   await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in javascript:
                                    cargo = discord.utils.get(server.roles, name="</Helper JavaScript>")
                                    await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in kotlin:
                                     cargo = discord.utils.get(server.roles, name="</Helper Kotlin>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in java:
                                     cargo = discord.utils.get(server.roles, name="</Helper Java>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in ruby:
                                     cargo = discord.utils.get(server.roles, name="</Helper Ruby>")
                                     await ctx.author.add_roles(cargo)
                                 elif lang2.content.lower() in go:
                                     cargo = discord.utils.get(server.roles, name="</Helper Golang>")

                           elif reaction.emoji.name == 'errado':
                                   await msg.delete()
                                   embed = discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Diga-me o motivo da recusa do **Helper** ``{str(ctx.author)}``", color=0x7BCDE8)
                                   server = self.bot.get_guild(self.bot.guild)
                                   channel = discord.utils.get(server.channels, id=self.bot.helper)
                                   await channel.send(embed=embed)                                   
                                   recused = await self.bot.wait_for('message') 
                                   if recused.content.lower().startswith("motivo :"):
                                       await msg.delete()
                                       embed = discord.Embed(color=self.bot.cor)
                                   
                                       embed.add_field(name=":bell: Motivo", value = "``"+str(recused.content)+"``", inline=True)
                                       embed.set_thumbnail(url=ctx.author.avatar_url_as())
                                       embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
                                       server = self.bot.get_guild(self.bot.guild)
                                      #canal solicitação
                                       channel = discord.utils.get(server.channels, id=self.bot.helper)
                                       await channel.send(recused.content)
         except asyncio.TimeoutError:
             self.forms.remove(ctx.author.id)             
             await msg.delete()
             embed=discord.Embed(description=f"{self.bot._emojis['timer']} **|** Olá **{ctx.author.name}**, passou do tempo limite e por isso a cadastramento foi cancelado.", color=0x7BCDE8)
             msg = await ctx.author.send(embed=embed)
             await asyncio.sleep(30)
             await msg.delete()


        except discord.errors.Forbidden:
             self.forms.remove(ctx.author.id)
             await msg.delete()
             embed=discord.Embed(description=f":envelope_with_arrow:**|** Olá **{ctx.author.name}**, para iniciar o processo precisamos que você libere suas mensagens privadas.", color=0x7BCDE8)
             msg = await ctx.send(embed=embed)
             await asyncio.sleep(30)
             await msg.delete()
                      


def setup(bard):
    bard.add_cog(helper(bard))
