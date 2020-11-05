
import discord
from discord.ext import commands
import random
import time
import asyncio
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo import MongoClient
from asyncio import TimeoutError as Esgotado
from datetime import datetime
import pymongo
import json

startTime = time.time()
def getUptime():
  return time.time() - startTime  

timetime=dict()

prefixos = ["c.","!","@","/"]
python = ['python', 'py']
javascript = ['javascript','js']
kotlin = ['kotlin','kt']
java = ['java']
ruby = ['ruby','rb']
go = ['golang', 'go']
linguagem = ["python","javascript","java","kotlin","golang","ruby","nenhuma"]
blocklist = []

class Desenvolvimento(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.users = []
      self.forms = []
      self.linguagens = {
            "py": {
                "aliases": ["python", "py", "discord.py"],
                "nome": "Python",
                "cor": 0x007AFF,
                "author": "COMANDOS NA LINGUAGEM PYTHON:",
                "logo": "https://imgur.com/LD60DLf.png"
            },
            "js": {
                "aliases": ["javascript", "js", "discord.js", "node", "node.j"],
                "nome": "JavaScript",
                "cor": 0xFF4500,
                "author": "COMANDOS NA LINGUAGEM JAVASCRIPT:",
                "logo": "https://imgur.com/T0RjAz1.png"
            }
        }
    
   @commands.bot_has_permissions(embed_links=True)
   @commands.cooldown(1,10,commands.BucketType.user)
   @commands.guild_only()
   @commands.command(description='Dê um ponto de reputação para quando um </New Helper> lhe ajudar.',usage='c.rep @</New Helper>')
   async def rep(self, ctx, *, user: discord.Member = None):
         if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
         if user is None:
            embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, mencione o usuário que você gostaria de dá a reputação.", color=self.bot.cor)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(20)
            await msg.delete()              
            return
         else:
            usuario = user
            if usuario.bot is True:
               embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, não é possível dá reputação ao um **BOT**.", color=self.bot.cor)
               msg = await ctx.send(embed=embed)
               await asyncio.sleep(20)
               await msg.delete()              
               return
            if not str("</Helper>") in [r.name for r in user.roles if r.name != "@everyone"]:
                embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, o usuário {user.mention} não é um **</Helper>** registrado.", color=self.bot.cor)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(20)
                await msg.delete()              
                return
            if ctx.author.id == user.id:
               embed=discord.Embed(description=f"{{self.bot._emojis['incorreto']}} **|** Olá **{ctx.author.name}**, não é possível dá reputação a si mesmo.", color=self.bot.cor)
               msg = await ctx.send(embed=embed)
               await asyncio.sleep(20)
               await msg.delete()              
               return
             
            if ctx.author.id in timetime:
               w = json.loads(timetime[ctx.author.id])
               if time.time() < w:
                  w = int(w) - int(time.time())
                  minute = 60
                  hour = minute * 60
                  day = hour * 24
                  days =  int(w / day)
                  hours = int((w % day) / hour)
                  minutes = int((w % hour) / minute)
                  seconds = int(w % minute)
                  string = ""
                  if days > 0:
                     string += str(days) + " " + (days == 1 and "dia" or "dias" ) + ", "
                  if len(string) > 0 or hours > 0:
                     string += str(hours) + " " + (hours == 1 and "hora" or "horas" ) + ", "
                  if len(string) > 0 or minutes > 0:
                     string += str(minutes) + " " + (minutes == 1 and "minuto" or "minutos" ) + ", "
                  string += str(seconds) + " " + (seconds == 1 and "segundo" or "segundos" )
                  embed=discord.Embed(description=f"{self.bot._emojis['timer']} **|** Olá **{ctx.author.name}**, você precisa esperar **{str(string)}** para da uma nova reputação ao usuário.", color=self.bot.cor)
                  await ctx.send(embed=embed)
                  return
            mongo = MongoClient(self.bot.database)
            bard = mongo['bard']
            users = bard['users']
            usuario = bard.users.find_one({'_id': str(usuario.id)})
            if usuario is None:
               embed=discord.Embed(description=f"{self.bot._emojis['correto']} **|** Olá **{ctx.author.name}**, você deu **1** ponto de reputação ao usuário {user.mention}.", color=self.bot.cor)
               await ctx.send(embed=embed)
               rep = int(usuario["reputação"])+int(1)
               bard.users.update_one({'_id': str(user.id)}, {'$set': {'reputação':int(rep)}})
            else:
               embed=discord.Embed(description=f"{self.bot._emojis['correto']} **|** Olá **{ctx.author.name}**, você deu **1** de reputação ao usuário {user.mention}.", color=self.bot.cor)
               await ctx.send(embed=embed)
               rep = int(usuario["reputação"])+int(1)
               bard.users.update_one({'_id': str(user.id)}, {'$set': {'reputação':int(rep)}})

   @rep.error
   async def rep_error(self, ctx, error):
      if isinstance(error, commands.BadArgument):
         comma = error.args[0].split('"')[1]
         embed = discord.Embed(title=f"{self.bot._emojis['incorreto']} | MEMBRO INVÁLIDO!", color=self.bot.cor, description=f"O membro `{comma}` não foi encontrado.")
         await ctx.send(embed=embed)
         ctx.command.reset_cooldown(ctx)
         return
       

   


   @commands.command()
   async def reps(self, ctx, membro: discord.Member = None):
         if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
            await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
            return
         if membro is None:
            usuario = ctx.author
            titulo = f"Olá {usuario.name}, veja a sua quantidade de rep's a baixo."
         else:
              usuario = membro
              titulo = f"Olá {ctx.author.name}, veja a quantidade de rep's de `{usuario.name}` abaixo."
         embed = discord.Embed(description=titulo,colour=self.bot.cor)
         mongo = MongoClient(self.bot.database)
         bard = mongo['bard']
         users = bard['users']
         users = bard.users.find_one({"_id": str(usuario.id)})
         if not users is None:
            embed.add_field(name=f"Reputação:", value =  "``"+str(users["reputação"])+"``", inline=True)
         if users is None:
            return await ctx.send(f'**{ctx.author.name}** o usuário `{membro.name}` não está registrado.')
        
         await ctx.send(embed=embed)

   @commands.command(
        name='comandos',
        aliases=['cmds'],
        description='Mostra a lista de todos os comandos registrados no sistema pra linguagem especificada',
        usage='c.comandos [py|js]'
    )
   async def _comandos(self, ctx, linguagem):
      if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
        await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        return
      linguagens = self.linguagens
      linguagem = linguagem.lower()
      

      if linguagem not in linguagens['js']['aliases'] and linguagem not in linguagens['py']['aliases']:
         return await ctx.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, você não especificou uma linguagem válida!\n**Linguagens disponíveis**: `py` e `js`")

      linguagem = linguagens['py'] if linguagem in linguagens['py']['aliases'] else linguagens['js']

      em = discord.Embed(
         colour=self.bot.cor,
         description=" , ".join([f"**`{c['nome']}`**" for c in self.bot.db.cmds.find({"linguagem": linguagem['nome'].lower(), "pendente": False}).sort("vPositivos", DESCENDING)]))
      em.set_author(name=linguagem['author'],icon_url=linguagem['logo'])
      em.set_footer(
         text=self.bot.user.name+" © 2020",
         icon_url=self.bot.user.avatar_url_as()
      )

      await ctx.send(embed=em)

   @commands.command(
      name='comandopy',
      aliases=['cmdpy'],
      description='Visualiza o código de um comando em Python publicado por um membro',
      usage='c.comandopy <Nome do Comando>'
   )
   @commands.cooldown(1, 10, commands.BucketType.user)
   @commands.bot_has_permissions(embed_links=True)
   async def _comandopy(self, ctx, *, nome):
      if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
        await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        return
      cmd = self.bot.db.cmds.find_one({"linguagem": "python", "nome": nome.lower(), "pendente": False})
      if cmd is None:
         return await ctx.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, não foi possível encontrar um comando em `Python` com o nome ``{nome}``.")
      

      try:
         autor = await self.bot.fetch_user(int(cmd['autor']))
      except:
         autor = "Não encontrado"

      data = cmd['data'].strftime("%d/%m/20%y - %H:%M:%S")

      em = discord.Embed(
         colour=self.bot.cor,
         description=f"\n**NOME DO COMANDO:** ``{nome.lower()}``\n**AUTOR:** `{autor}`\n**DATA DE ENVIO:** `{data}`\n```py\n{cmd['code']}```")
      #em.set_footer(
         #text=f"👍 {cmd['vPositivos']} votos e {cmd['vNegativos']} votos Negativos",)
      #em.set_thumbnail(url="https://imgur.com/LD60DLf.png")
      em.set_footer(
         text=self.bot.user.name+" © 2020",
         icon_url=self.bot.user.avatar_url_as()
      )

      await ctx.send(embed=em)

   @commands.command(
      name='comandojs',
      aliases=['cmdjs'],
      description='Visualiza o código de um comando em JavaScript publicado por um membro',
      usage='c.comandojs <Nome do Comando>'
   )
   @commands.cooldown(1, 10, commands.BucketType.user)
   @commands.bot_has_permissions(embed_links=True)
   async def _comandojs(self, ctx, *, nome = None):
      if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
        await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        return
      cmd = self.bot.db.cmds.find_one({"linguagem": "javascript", "nome": nome.lower(), "pendente": False})
      if cmd is None:
         return await ctx.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, não foi possível encontrar um comando em `Python` com o nome ``{nome}``.")
      

      try:
         autor = await self.bot.fetch_user(int(cmd['autor']))
      except:
         autor = "Não encontrado"

      data = cmd['data'].strftime("%d/%m/20%y - %H:%M:%S")

      em = discord.Embed(
         colour=self.bot.cor,
         description=f"\n**NOME DO COMANDO:** ``{nome.lower()}``\n**AUTOR:** `{autor}`\n**DATA DE ENVIO:** `{data}`\n```py\n{cmd['code']}```")
      #em.set_footer(
         #text=f"👍 {cmd['vPositivos']} votos e {cmd['vNegativos']} votos Negativos",)
      #em.set_thumbnail(url="https://imgur.com/LD60DLf.png")
      em.set_footer(
         text=self.bot.user.name+" © 2020",
         icon_url=self.bot.user.avatar_url_as()
      )

      await ctx.send(embed=em)

   @commands.command(
      name='enviarcomando',
      aliases=['enviarcmd', 'adicionarcomando', 'addcomando','addcmd'],
      description='Envia um código de comando para aprovação',
      usage='c.enviarcomando'
   )
   @commands.cooldown(1, 12, commands.BucketType.user)
   async def _enviarcomando(self, ctx):
      if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
        await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        return
      reactions = [":errado:761205727841746954", ':like:760197986609004584']
      if ctx.author.id in self.users:
         return await ctx.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, já tem um formulário em aberto no seu DM.", delete_after=30)

      try:
         nome = discord.Embed(description=f"<:newDevs:573629564627058709> **|** Então você quer adicionar um **Comando** no NewDevs?\nPara isso precisamos que você preencha um pequeno formulário para cadastramento de seu **comando** em nosso sistema.\n\n{self.bot._emojis['nome']} **|** Diga-nos o nome do **comando**: \n{self.bot._emojis['timer']} **|** **2 minutos**", color=self.bot.cor)
         msg_nome = await ctx.author.send(embed=nome, delete_after=120)
      except:
         await ctx.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, você precisa ativar as **`Mensagens Diretas`** para que eu possa prosseguir com o formulário de adicionar comandos.")
      
      self.users.append(ctx.author.id)
      embed = discord.Embed(description=f":envelope_with_arrow: **|** Olá **{ctx.author.name}**, verifique sua mensagens diretas (DM).", color=self.bot.cor)
      await ctx.send(embed=embed)

      def check(m):
         return m.channel.id == msg_nome.channel.id and m.author == ctx.author

      nome = None
      limite = 12
      tentativas = 0
      while nome is None:
         try:
               resposta = await self.bot.wait_for("message", check=check, timeout=120)
         except Esgotado:
               
               await ctx.author.send(f"{self.bot._emojis['seta']} | **{ctx.author.name}**, você demorou muito para fornecer um nome!", delete_after=30)
               break

         if tentativas == 3:
               await ctx.author.send(f"{self.bot._emojis['incorreto']} **{ctx.author.name}**, você atingiu o limite de 3 tentativas e por isso a ação foi cancelada.", delete_after=20)
               break
         elif len(resposta.content) > limite:
               tentativas += 1
               await ctx.author.send(f"{self.bot._emojis['seta']} O **`nome`** fornecido é muito grande! **Máximo de {limite} caracteres\nTentativa: `{tentativas}/3`**", delete_after=15)
         else:
               nome = resposta.content
      
      if not nome:
         return self.users.remove(ctx.author.id)

      nome = nome.lower()
   
      embed=discord.Embed(description=f"{self.bot._emojis['api']} **|** Agora diga-me a linguagem que o **comando** foi feito\n{self.bot._emojis['api']} Linguagens : [**PYTHON | JAVASCRIPT**]\n{self.bot._emojis['timer']} **|** **2 minutos**", color=self.bot.cor)
      msg_lang = await ctx.author.send(embed=embed)
      
      def check_author1(m):
         return m.author == ctx.author and m.guild is None

      linguagem = None
      linguagens = self.linguagens
      tentativas = 0
      while linguagem is None:
         try:
               resposta = await self.bot.wait_for("message", check=check_author1, timeout=120)
         except Esgotado:
               await ctx.author.send(f" | **{ctx.author.name}**, você demorou muito para especificar a linguagem!", delete_after=30)
               break

         if tentativas == 3:
               await ctx.author.send(f" **{ctx.author.name}**, você errou e atingiu o máximo de tentativas permitidas. `(3)`", delete_after=20)
               break
         elif resposta.content.lower() not in linguagens['py']['aliases'] and resposta.content.lower() not in linguagens['js']['aliases']:
               tentativas += 1
               await ctx.author.send(f"{self.bot._emojis['seta']} A **`linguagem`** especificada é inválida! **Linguagens permitidas: `Python`**, **`JavaScript`\nTentativa: `{tentativas}/3`**", delete_after=15)
         else:
               linguagem = resposta.content
      
      if not linguagem:
         return self.users.remove(ctx.author.id)

      linguagem = linguagens['py'] if linguagem.lower() in linguagens['py']['aliases'] else linguagens['js']
      #       < < < ------------------------------------- > > >

      comando = self.bot.db.cmds.find_one({"linguagem": linguagem['nome'].lower(), "nome": nome})
      if comando:
         self.users.remove(ctx.author.id)
         return await ctx.author.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, já temos um comando chamado **`{nome}`** para a linguagem **`{linguagem['nome']}`**.")

      #       < < < ------------------------------------- > > >
      texto = f"{self.bot._emojis['api']} **|** Agora cole-o **comando** ou escreva ele. (limite 2000 caracteres)\n{self.bot._emojis['timer']} **|** **2 minutos**"
      embed=discord.Embed(description=texto, color=self.bot.cor)
      msg_code = await ctx.author.send(embed=embed)
      
      def check_author(m):
         return m.author == ctx.author and m.guild is None

      code = None
      limite = 2000
      tentativas = 0
      while code is None:
         try:
               resposta = await self.bot.wait_for("message", check=check_author, timeout=300)
         except Esgotado:
               await ctx.author.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, você demorou muito para especificar a linguagem!", delete_after=30)
               break

         if tentativas == 3:
               await ctx.author.send(f"{self.bot._emojis['incorreto']} **{ctx.author.name}**, você atingiu o limite de 3 tentativas e por isso a ação foi cancelada.", delete_after=20)
               break
         elif len(resposta.content) > limite:
               tentativas += 1
               embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, o **código** do comando que você inseriu passou do limite de 2000 caracteres.\n\n{self.bot._emojis['seta']} | **Tentativa: `{tentativas}/3`**", color=self.bot.cor)
               await ctx.author.send(embed)
               #await ctx.author.send(f"{self.bot._emojis['seta']} Seu código ultrapassa o limite de **`{limite}`** caracteres permitidos.\n**Tentativa: `{tentativas}/3`**", delete_after=15)
         else:
               #embed=discord.Embed(description=f"{self.bot._emojis['incorreto']} **|** Seu comando foi enviado para análise e informaremos o fututo dele no canal <#773555758632796251>.", color=self.bot.cor)
               #await ctx.author.send(embed)
               code = resposta.content
      
      if not code:
         return self.users.remove(ctx.author.id)
      #       < < < ------------------------------------- > > >

      embed=discord.Embed(description=f"```{linguagem['nome'].lower()}\n{code}\n```", color=self.bot.cor,timestamp=datetime.utcnow())
      embed.set_author(name="SOLICITAÇÃO ADICIONAR COMANDO", icon_url=ctx.author.avatar_url_as())
      embed.add_field(name=f"{self.bot._emojis['nome']} Nome", value = "``"+str(nome)+"``", inline=True)
      embed.add_field(name=f"{self.bot._emojis['api']} Linguagem ", value = "``"+str(linguagem['nome'])+"``", inline=True)
      embed.add_field(name=f"{self.bot._emojis['mention']} Enviado por", value = "``"+str(ctx.author)+"`` ("+str(ctx.author.mention)+")", inline=True)
      embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
      
   
      
      logs = self.bot.get_channel(773555758632796251)
      aprovar_comandos = self.bot.get_channel(772972566402826242)
      #pendente_msg = await aprovar_comandos.send(embed=em, content="**NOVO COMANDO AGUARDANDO POR APROVAÇÃO!**")
      pendente_msg = await aprovar_comandos.send(embed=embed, content="@here")

      await logs.send(f"{self.bot._emojis['discord']} {ctx.author.mention} enviou o comando **`{nome}`** para verificação.")
      for e in reactions:
         await pendente_msg.add_reaction(e)

      self.bot.db.cmds.insert_one({
         "_id": pendente_msg.id,
         "linguagem": linguagem['nome'].lower(),
         "nome": nome,
         "code": code,
         "autor": ctx.author.id,
         "categoria": None,
         "vMembros": [],
         "vPositivos": 0,
         "vNegativos": 0,
         "aprovado_por": None,
         "data": datetime.now(),
         "pendente": True,
         "pendente_msg": pendente_msg.id
      })

      await ctx.author.send(f"{self.bot._emojis['correto']} | Seu comando **`{nome}`** na linguagem **`{linguagem['nome']}`** foi enviado para a verificação.")
      self.users.remove(ctx.author.id)

   @commands.Cog.listener()
   async def on_raw_reaction_add(self, payload):
      if payload.channel_id != 772972566402826242 or payload.user_id == self.bot.user.id:
         return

      comando = self.bot.db.cmds.find_one({"pendente": True, "pendente_msg": payload.message_id})
      if not comando:
         return

      logs = self.bot.get_channel(773555758632796251)
      canal = self.bot.get_channel(payload.channel_id)
      mensagem = await canal.fetch_message(payload.message_id)
      staffer = mensagem.guild.get_member(payload.user_id)
      autor = mensagem.guild.get_member(comando['autor'])
      if str(payload.emoji) == self.bot._emojis['correto']:
         self.bot.db.cmds.update_one(comando, {"$set": {"pendente": False, "aprovado_por": payload.user_id}})
         await logs.send(f"{self.bot._emojis['correto']} O comando **`{comando['nome']}`** enviado por <@{comando['autor']}> foi aprovado por **{staffer.name}**.")
         await mensagem.delete()

         if autor:
               try:
                  await autor.send(f"{self.bot._emojis['correto']} | **{autor.name}**, seu comando **`{comando['nome']}`** foi aceito por **{staffer.name}**.")
               except:
                  pass
      elif str(payload.emoji) == self.bot._emojis['errado']:
         enviador = await self.bot.fetch_user(comando['autor'])
         try:
               embed = discord.Embed(description=f"{self.bot._emojis['api']} | **INFORME O MOTIVO DE ESTAR RECUSANDO O COMANDO `{comando['nome'].title()}`**.\n\n{self.bot._emojis['timer']} | **`5 minutos`**", color=self.bot.cor)
               embed.set_footer(text=f"Autor: {enviador}.",icon_url=enviador.avatar_url_as(format="png"))
               pergunta = await staffer.send(embed=embed)
         except:
               await mensagem.remove_reaction(payload.emoji, staffer)
               return await canal.send(f"{self.bot._emojis['discord']} {staffer.mention}, **você precisa ativar as DMs para prosseguir**.")

         def check(m):
               return m.channel.id == pergunta.channel.id and m.author == staffer
      
         try:
               resposta = await self.bot.wait_for("message", check=check, timeout=300)
         except Esgotado:

               embed=discord.Embed(colour=self.bot.cor, description=f"{self.bot._emojis['incorreto']} | **{staffer.name}**, você demorou demais para fornecer um motivo.")
               await mensagem.remove_reaction(payload.emoji, staffer)
               return await staffer.send(embed=embed)
         
         embed=discord.Embed(colour=self.bot.cor, description=f"{self.bot._emojis['correto']} **{staffer.name}**, você recusou o comando `{comando['nome']}`.\n\n{self.bot._emojis['tipo']} | **MOTIVO:** ```{resposta.content}```")
         embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
         await staffer.send(embed=embed)
         await logs.send(f"{self.bot._emojis['errado']} **{staffer.name}** rejeitou o comando **`{comando['nome']}`** enviado por <@{comando['autor']}>.")

         if autor:
               try:
                  embed=discord.Embed(colour=self.bot.cor, description=f"{self.bot._emojis['incorreto']} **{autor.name}**, seu comando **`{comando['nome']}`** foi recusado.\n{self.bot._emojis['mention']} | **STAFFER:** ``{staffer}``\n\n{self.bot._emojis['tipo']} | **MOTIVO:** ```{resposta.content}```")
                  embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
                  #await autor.send(f"{self.bot._emojis['incorreto']} | **{autor.name}**, seu comando **`{comando['nome']}`** foi recusado por **{staffer.name}**.```Motivo: {resposta.content}```")
                  await autor.send(embed=embed)
               except:
                  pass
         
         self.bot.db.cmds.delete_one(comando)
         await mensagem.delete()


   @commands.cooldown(1,10,commands.BucketType.user)
   @commands.guild_only()
   @commands.bot_has_permissions(embed_links=True)
   @commands.command(hidden=True)
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
                              channel = discord.utils.get(server.channels, id=772972566402826242)
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
                     





def setup(bot):
    bot.add_cog(Desenvolvimento(bot))
