import discord
from discord.ext import commands
from utils import botstatus
from urllib.request import Request, urlopen
import urllib
import sys
from datetime import datetime, timedelta
import discord
import requests

def perms_check(role):
    list_perms = ['empty']
    for perm in role:
        if perm[1] is True:
            if 'empty' in list_perms:
                list_perms = list()
            list_perms.append(perm[0])
    if 'empty' not in list_perms:
        all_perms = ", ".join(list_perms)
        return all_perms
    else:
        return "O cargo mencionado não tem nenhuma permissão."


class informacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='envia a sua foto de perfil ou a de um usuário.',usage='c.avatar',aliases=['pic'])
    async def avatar(self, ctx, *, user: discord.Member = None):
      if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
        await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        return
      if user is None:
          usuario = ctx.author.avatar_url
          texto = f"Olá {ctx.author.name}, está é sua imagem de perfil."
      else:
          usuario = user.avatar_url
          texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name}"

      embed = discord.Embed(title=texto, color=self.bot.cor)
      embed.set_image(url=usuario)
      embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
      await ctx.send(embed=embed)
  
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Mostra algumas informações sobre mim.',usage='c.botinfo',aliases=['bot'])
    async def botinfo(self,ctx):
      if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
        await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        return
      mem = botstatus.get_memory()
      dono = await self.bot.fetch_user(478266814204477448)
      embed = discord.Embed(description="Olá {}, este é o perfil do {} e nele contém algumas informações.".format(ctx.author.name, self.bot.user.name),colour=self.bot.cor)
      embed.set_author(name="Informações do {}".format(self.bot.user.name), icon_url=ctx.author.avatar_url_as())
      embed.add_field(name=f"{self.bot._emojis['dono']} Criador", value = f'``{dono}``')
      embed.add_field(name=f"{self.bot._emojis['tag']} Tag", value = '``'+str(self.bot.user)+'``')
      embed.add_field(name=f"{self.bot._emojis['ip']} ID", value = '``'+str(self.bot.user.id)+'``')
      embed.add_field(name=f"{self.bot._emojis['api']} Api", value = '``Discord.py '+str(discord.__version__)+'``')
      embed.add_field(name=f"{self.bot._emojis['python']} Python", value = '``'+str(sys.version[:5])+'``')
      embed.add_field(name=f"{self.bot._emojis['ram']} Memória", value = '``'+str(mem["memory_used"])+'/'+str(mem["memory_total"])+' ('+str(mem["memory_percent"])+')``')
      embed.add_field(name=f"{self.bot._emojis['timer']} Tempo de atividade", value = '``'+str(botstatus.timetotal()).replace("{day}","dia").replace("{hour}","hora").replace("{minute}","minuto").replace("{second}","segundo")+'``')
      embed.add_field(name=f"{self.bot._emojis['guilds']} Servidores", value = '``'+str(len(self.bot.guilds))+' (shards '+"1"+')``')
      embed.add_field(name=f"{self.bot._emojis['ping']} Lâtencia", value = '``{0:.2f}ms``'.format(self.bot.latency * 1000))
      embed.add_field(name=f"{self.bot._emojis['cpu']} Porcentágem da CPU",value=f'``{botstatus.cpu_usage()}%``')
      #embed.add_field(name=f"<:ping:564890304839417887> Processador", value=f'``{botstatus.host_name()}``')
      embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
      await ctx.send(embed=embed)
    

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.command(description='Mostra todas as informações do seu servidor.',usage='c.serverinfo',aliases=['sinfo', 'guildinfo'])
    async def serverinfo(self, ctx):
      if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
        await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        return
      servidor = ctx.guild
      if servidor.icon_url_as(format="png") == "":
        img = "https://i.imgur.com/To9mDVT.png"
      else:

        img  = servidor.icon_url
        online = len([y.id for y in servidor.members if y.status == discord.Status.online])
        afk  = len([y.id for y in servidor.members if y.status == y.status == discord.Status.idle])
        offline = len([y.id for y in servidor.members if y.status == y.status == discord.Status.offline])
        dnd = len([y.id for y in servidor.members if y.status == y.status == discord.Status.dnd])
        geral = len([y.id for y in servidor.members])
        bots= len([y.id for y in servidor.members if y.bot])
        criado_em = str(servidor.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
        dias = (datetime.utcnow() - servidor.created_at).days
        usuarios = " <:nsonline:761304111152758846> : ``"+str(online)+"``<:nsocupado:761304111017754635> : ``"+str(afk)+"``  <:nsdnd:761304111336783872> : ``"+str(dnd)+"`` <:nsoffline:761304111361556520> : ``"+str(offline)+f"`` {self.bot._emojis['bots']} : ``"+str(bots)+"``"
        texto = f"{self.bot._emojis['texto']} : ``"+str(len(servidor.text_channels))+f"``{self.bot._emojis['voz']}  : ``"+str(len(servidor.voice_channels))+"``"
        cargos = len([y.id for y in servidor.roles])
        emojis = len([y.id for y in servidor.emojis])
        embed = discord.Embed(description="Olá {}, aqui estão todas as informaçôes do servidor `{}`.".format(ctx.author.name, servidor.name),colour=self.bot.cor)
        embed.set_author(name=f"Informação do servidor", icon_url=ctx.author.avatar_url_as())
        embed.add_field(name=f"{self.bot._emojis['dono']} Dono", value = "``"+str(servidor.owner)+"``")
        embed.add_field(name=f"{self.bot._emojis['nome']} Nome", value = "``"+str(servidor.name)+"``")
        embed.add_field(name=f"{self.bot._emojis['ip']} Id", value = "``"+str(servidor.id)+"``")
        embed.add_field(name=f"{self.bot._emojis['notas']} Criação", value =f"``{criado_em}`` ({dias} dias)")
        embed.add_field(name=f"{self.bot._emojis['roles']} Cargos", value = "``"+str(cargos)+"``")
        embed.add_field(name=f"{self.bot._emojis['emoji']} Emojis", value = "``"+str(emojis)+"``")
        embed.add_field(name=f"{self.bot._emojis['canais']} Canais", value = texto)
        embed.add_field(name=f"{self.bot._emojis['local']} Localização", value = "``"+str(servidor.region).title()+"``")
        embed.add_field(name=f"{self.bot._emojis['cadeado']} Verificação", value = "``"+str(servidor.verification_level).replace("none","Nenhuma").replace("low","Baixa").replace("medium","Média").replace("high","Alta").replace("extreme","Muito alta")+"``")
        embed.add_field(name=f" Usuários"+" ["+str(geral)+"]", value = usuarios)
        embed.set_thumbnail(url=img)
        embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed = embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.command(description='Mostra as informações de um usuário.',usage='c.userinfo @TOBIAS',aliases=['uinfo', 'usuario'])
    async def userinfo(self, ctx, *, user: discord.Member = None):
      if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
        await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        return
      if user is None:
        usuario = ctx.author
        titulo = "Olá {}, esse é o seu perfil e aqui estão suas informações.".format(ctx.author.name)
      else:
        usuario = user
        titulo = "Olá {}, este é o perfil de {} e nele contém umas informações.".format(ctx.author.name, usuario.name)

      if usuario.display_name == usuario.name:
          apelido = "Não defindo"
      else:
        apelido = usuario.display_name
      if usuario.avatar_url_as()  == "":
        img = "https://i.imgur.com/To9mDVT.png"
      else:
        img = usuario.avatar_url_as()
      try:
        jogo = usuario.activity.name
      except:
          jogo = "No momento nada."
      if usuario.id in [y.id for y in ctx.guild.members if not y.bot]:
        bot = "Não"
      else:
        bot = "Sim"
      svs = ', '.join([c.name for c in self.bot.guilds if usuario in c.members])
      entrou_servidor = str(usuario.joined_at.strftime("%d/%m/20%y ás %H:%M:%S"))
      conta_criada = str(usuario.created_at.strftime("%d/%m/20%y"))
      conta_dias = (datetime.utcnow() - usuario.created_at).days
      cargos = len([r.name for r in usuario.roles if r.name != "@everyone"])
      if not svs: 
        svs = 'Nenhum servidor em comum.'
      on = "Disponível"
      off = "Offline"
      dnd = "Não Pertubar"
      afk = "Ausente"
      stat = str(usuario.status).replace("online",on).replace("offline",off).replace("dnd",dnd).replace("idle",afk)
      cargos2 = len([y.id for y in ctx.guild.roles])
      embed = discord.Embed(description=titulo,colour=self.bot.cor)
      embed.set_author(name=f"Informação de perfil", icon_url=ctx.author.avatar_url_as())
      embed.add_field(name=f"{self.bot._emojis['tag']} Tag", value = "``"+str(usuario.name)+"#"+str(usuario.discriminator)+"``")
      embed.add_field(name=f"{self.bot._emojis['ip']} Id", value = "``"+str(usuario.id)+"``")
      embed.add_field(name=f"{self.bot._emojis['nome']} Apelido", value = "``"+str(apelido)+"``")
      embed.add_field(name=f"{self.bot._emojis['notas']} Criação da conta", value =f"``{conta_criada}`` ({conta_dias} dias)")
      embed.add_field(name=f"{self.bot._emojis['entrou']} Entrou aqui em", value = "``"+str(entrou_servidor)+"``")
      embed.add_field(name=f"{self.bot._emojis['toprole']} Maior cargo", value = "``"+str(usuario.top_role)+"``")
      embed.add_field(name=f"{self.bot._emojis['roles']} Cargos", value = "``"+str(cargos)+"/"+str(cargos2)+"``")
      embed.add_field(name=f"{self.bot._emojis['bots']} Bot", value = "``"+str(bot)+"``")
      embed.add_field(name=f"{self.bot._emojis['status']} Status", value = "``"+str(stat)+"``")
      embed.add_field(name=f"{self.bot._emojis['discord']} Servidores em comun",value=f"`{svs}`")
      embed.set_thumbnail(url=img)
      embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
      await ctx.send(embed = embed)


    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Mostra as informações de um canal.',usage='c.channelinfo #canal',aliases=['canalinfo', 'cinfo'])
    async def channelinfo(self, ctx, *, num=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if num is None:
          num = ctx.channel.id
        if str(num).isdigit() == True:
          channel = discord.utils.get(ctx.guild.channels, id=int(num))
        else:
          if "<#" in num:
            num = str(num).replace("<#","").replace(">","")
            channel = discord.utils.get(ctx.guild.channels, id=int(num))
          else:
            channel = discord.utils.get(ctx.guild.channels, name=num)
        if channel is None:
          embed = discord.Embed(description="{} **|** O canal {} não existe.".format(self.bot._emojis['help'], num), color=self.bot.cor)
          await ctx.send(embed=embed)
          return  

        if channel in list(ctx.guild.text_channels):
          channel_type = "Texto"
        elif channel in list(ctx.guild.voice_channels):
          channel_type = "Audio"
        else:
          embed = discord.Embed(description="{} **|** O canal {} não existe.".format(self.bot._emojis['help'], num), color=self.bot.cor)
          await ctx.send(embed=embed)
          return  
         
        channel_created = str(channel.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
        embed = discord.Embed(description="Olá {}, esta são as informações do canal {}.".format(ctx.author.name, channel.mention),colour=self.bot.cor)
        embed.set_author(name=f"Informações do canal", icon_url=ctx.author.avatar_url_as())
        embed.add_field(name=f"{self.bot._emojis['nome']} Nome", value = "``"+str(channel.name)+"``",inline=False)
        embed.add_field(name=f"{self.bot._emojis['ip']} ID", value = "``"+str(channel.id)+"``",inline=False)
        embed.add_field(name=f"{self.bot._emojis['notas']} Criação", value = "``"+str(channel_created)+"``",inline=False)
        embed.add_field(name=f"{self.bot._emojis['canais']} Posição", value = "``"+str(channel.position)+"``",inline=False)
        embed.add_field(name=f"{self.bot._emojis['tipo']} Tipo do canal", value = "``"+str(channel_type)+"``",inline=False)
        try:
          embed.add_field(name=f"{self.bot._emojis['porn']} +18", value = "```"+str(channel.is_nsfw()).replace("False","Não").replace("True","Sim")+"```",inline=False)
          if channel.slowmode_delay == 0:
            valor = "Não definido"
          else:
            valor = "{} segundos".format(channel.slowmode_delay)
          embed.add_field(name=f"{self.bot._emojis['timer']} Slowmode", value = "``"+str(valor)+"``",inline=False)
          if channel.topic is None:
            topic = "Não definido"
          else:
            topic = channel.topic
          embed.add_field(name=f"{self.bot._emojis['tpico']} Tópico", value = "``"+str(topic[:1024])+"``",inline=False)          
        except:
          pass
        try:
          embed.add_field(name=f"{self.bot._emojis['voz']} Bitrate", value = "``"+str(channel.bitrate)+"``")
          if channel.user_limit != 0:
            embed.add_field(name=f"{self.bot._emojis['pessoas']} Usuários conectados", value="``{}/{}``".format(len(channel.members), channel.user_limit),inline=False)
          else:
            embed.add_field(name=f"{self.bot._emojis['pessoas']} Usuários conectados", value="``{}``".format(len(channel.members)),inline=False)          
        except:
          pass         


        embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed = embed)

    

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.command(description='Mostra as informações de um cargo',usage='c.roleinfo dj',aliases=['rinfo'])
    async def roleinfo(self, ctx, *, role: discord.Role = None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if role is None:
            return await ctx.send(f'**{ctx.author.name}** você não mencionou um cargo.')
        criado_em = str(role.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
        embed = discord.Embed(color=self.bot.cor)
        embed.set_author(name="Informação do cargo", icon_url=ctx.author.avatar_url_as())
        embed.add_field(name=f"{self.bot._emojis['tag']} Nome:", value="``"+str(role.name)+"``")
        embed.add_field(name=f"{self.bot._emojis['ip']} ID:", value=f"``"+str(role.id)+"``")
        mention = f"{role.mentionable}"
        embed.add_field(name=f"{self.bot._emojis['mention']} Mencionável:", value=f"``{mention.replace('False','Não').replace('True', 'Sim')}``")
        embed.add_field(name=f"{self.bot._emojis['cor']} Cor:", value="``"+str(role.colour)+"``")
        separado = f"{role.hoist}"
        embed.add_field(name=f"{self.bot._emojis['canais']} Posição do Cargo:", value=f"``{role.position}º``")
        embed.add_field(name=f"{self.bot._emojis['separado']} Separado dos Membros:", value=f"``{separado.replace('True','Sim').replace('False','Não')}``")
        embed.add_field(name=f"{self.bot._emojis['notas']} Data de Criação:", value=f"``"+str(criado_em)+"``")
        embed.add_field(name=f"{self.bot._emojis['pessoas']} Membro(s) com o cargo:", value=f"``{len(role.members)}``")
        perm = f"{perms_check(role.permissions)}"
        embed.add_field(name=f"{self.bot._emojis['cadeado']} Permissões:", value=f"``{perm.replace('use_voice_activation','Usar detecção de voz').replace('add_reactions','Adicionar reações').replace('administrator','Administrador').replace('attach_files','Anexar arquivos').replace('ban_members','Banir membros').replace('change_nickname','Mudar apelido').replace('connect','Conectar').replace('create_instant_invite','Criar um convite instatâneo').replace('deafen_members','Desativar áudio de membros').replace('embed_links','Inserir Links').replace('external_emojis','Emojis externos').replace('kick_members','Expulsar membros').replace('manage_channels','Gerenciar canais').replace('manage_emojis','Gerenciar emojis').replace('manage_guild','Gerenciar o servidor').replace('manage_messages','Gerenciar Mensagens').replace('manage_nicknames','Gerenciar apelidos').replace('manage_roles','Gerenciar cargos').replace('manage_webhooks','Gerenciar Webhooks').replace('mention_everyone','Mencionar todos').replace('move_members','Mover membros').replace('mute_members','Silenciar membros').replace('read_message_history','Ler histórico de mensagens').replace('read_messages','Ler mensagens').replace('send_messages','Enviar mensagens').replace('send_tts_messages','Enviar mensagem TTS').replace('speak','Falar').replace('view_audit_log','Ver registro de auditoria')}``")
        embed.set_thumbnail(url='https://htmlcolors.com/color-image/{}.png'.format(str(role.color).strip("#")))
        embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
        await ctx.send(embed=embed)

"""

    @commands.guild_only()
    @commands.command(aliases=["einfo", "infoemoji", "emoji", "emojinfo"])
    async def emojiinfo(self, ctx, *, emoji: discord.Emoji):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        embed = discord.Embed(color=self.bot.cor, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"Informações do emoji:", icon_url=emoji.url)
        embed.add_field(name=" Nome:", value=f"``{emoji.name}``",inline=False)
        coisa = f"{emoji.animated}"
        if emoji.animated:
            # if emoji.animated == 'True':
            embed.add_field(name=" Emoji Animado:", value=f"``Sim``", inline=False)
            # elif emoji.animated == 'False':
            #     embed.add_field(name="<:m_star:572234473605824532> Emoji Normal:", value=f"``Sim``", inline=False)
        else:
            embed.add_field(name=" Emoji Normal:", value=f"``Sim``", inline=False)
        embed.add_field(name=" ID", value=f"``{emoji.id}``", inline=False)
        embed.add_field(name=" Link:", value=f"[``Clique aqui``]({emoji.url})", inline=False)
        embed.add_field(name=" Adicionado em:", value=f"``{emoji.created_at.__format__('%d/%m/%Y às %H:%M')}``", inline=False)
        embed.set_thumbnail(url=emoji.url)
        embed.set_footer(text=f'{self.bot.user.name}© 2020', icon_url="https://i.imgur.com/Me7NqbZ.jpg") 
        await ctx.send(embed=embed)

    """

def setup(bot):
    bot.add_cog(informacao(bot))
