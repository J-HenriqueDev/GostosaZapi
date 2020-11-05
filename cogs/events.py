import discord
from unidecode import unidecode
from columnar import columnar
import asyncio
from datetime import datetime
import pytz
import requests, json, os
import re
from discord.ext import commands
from utils.Utils import difference_between_lists
aviso1 = []
aviso2 = []
aviso3 = []



class events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self , guild, member):
        await asyncio.sleep(3)
        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban ,limit=1):
            moderator = entry.user
            if moderator is None:
                moderator = "NADA"
            reason = entry.reason
            if reason is None:
                reason = "Não informada."
        embed = discord.Embed(color=self.bot.cor,timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
        embed.set_author(name=f"MEMBRO BANIDO", icon_url=guild.icon_url)
        embed.add_field(name=f"Usuário:", value=f"`{member.name}`")
        embed.add_field(name=f"Autor:",value=f"`{moderator}`")
        embed.add_field(name="Motivo:",value=f"``{reason}``")
        embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
        embed.set_thumbnail(url=member.avatar_url_as(format='png'))
        logs_bans = guild.get_channel(self.bot.bans)
        await logs_bans.send(embed=embed, content="<@&759814438323879987>")

    @commands.Cog.listener()
    async def on_member_unban(self , guild, member):
        await asyncio.sleep(3)
        moderator = 'Não encontrado.'
        async for entry in guild.audit_logs(action=discord.AuditLogAction.unban ,limit=1):
            moderator = entry.user
        embed = discord.Embed(color=self.bot.cor,timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
        embed.set_author(name=f"MEMBRO DESBANIDO", icon_url=guild.icon_url)
        embed.add_field(name=f"Usuário:", value=f"`{member.name}`")
        embed.add_field(name=f"Autor:",value=f"`{moderator}`")
        embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
        embed.set_thumbnail(url=member.avatar_url_as(format='png'))
        logs_bans = guild.get_channel(self.bot.bans)
        await logs_bans.send(embed=embed, content="<@&759814438323879987>")


    @commands.Cog.listener()
    async def on_member_kick(self , guild, member):
        await asyncio.sleep(3)
        async for entry in guild.audit_logs(action=discord.AuditLogAction.kick ,limit=1):
            moderator = entry.user
            if moderator is None:
                moderator = "NADA"
            reason = entry.reason
            if reason is None:
                reason = "Não informada."
        embed = discord.Embed(color=self.bot.cor,timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
        embed.set_author(name=f"MEMBRO KICKADO", icon_url=guild.icon_url)
        embed.add_field(name=f"Usuário:", value=f"`{member.name}`")
        embed.add_field(name=f"Autor:",value=f"`{moderator}`")
        embed.add_field(name="Motivo:",value=f"``{reason}``")
        embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
        embed.set_thumbnail(url=member.avatar_url_as(format='png'))
        logs_bans = guild.get_channel(self.bot.bans)
        await logs_bans.send(embed=embed, content="<@759814438323879987")



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
          comma = error.args[0].split('"')[1]
          quantidade = len(comma)
          if quantidade > 13:
            return await ctx.send('não tente me bugar poha')
          embed = discord.Embed(title=f"<:unlike:760197986592096256> | Comando não encontrado", color=self.bot.cor, description=f"O comando `{comma}` não existe.")
          await ctx.send(embed=embed)

        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument, commands.MissingRequiredArgument)):
          uso = ctx.command.usage if ctx.command.usage else "Não especificado."
          await ctx.send(f"{self.bot._emojis['incorreto']} **Oops**, **{ctx.author.name}**! Parece que você usou o comando **`{ctx.command.name}`** de forma errada!\nUso correto: **`{uso}`**")
        
        elif isinstance(error, commands.BotMissingPermissions):
            perms = '\n'.join([f"   {self.bot._emojis['incorreto']} **`{perm.upper()}`**" for perm in error.missing_perms])
            await ctx.send(f"**{ctx.author.name}**, eu preciso das seguintes permissões para poder executar o comando **`{ctx.invoked_with}`** nesse servidor:\n\n{perms}")
        
        elif isinstance(error, commands.MissingPermissions):
            perms = '\n'.join([f"   {self.bot._emojis['incorreto']} **`{perm.upper()}`**" for perm in error.missing_perms])
            await ctx.send(f"**{ctx.author.name}**, você precisa das seguintes permissões para poder usar o comando **`{ctx.invoked_with}`** nesse servidor:\n\n{perms}")

        elif isinstance(error, commands.CommandOnCooldown):
          s = divmod(error.retry_after, 60)
          return await ctx.send(f"**{ctx.author.name}**, aguarde **`{int(s)}`** segundo(s) para poder usar o comando **`{ctx.invoked_with}`** novamente.")
        
        elif isinstance(error, commands.CheckFailure):
            pass

        elif isinstance(error, commands.DisabledCommand):
          await ctx.send(f" <:unlike:760197986592096256> | **{ctx.author.name}**, o comando **`{ctx.invoked_with}`** está temporariamente desativado.")
        
        elif isinstance(error, commands.MissingRequiredArgument):
          await ctx.send('faltando argumentos')


        elif isinstance(error, commands.CommandError):
            logs = self.bot.get_channel(773515801793134602)
            em = discord.Embed(
                colour=self.bot.cor,
                description=f"```py\n{error}```",
                timestamp=ctx.message.created_at
            ).set_author(
                name=str(ctx.author),
                icon_url=ctx.author.avatar_url
            )
            await logs.send(embed=em, content="**Usuário: `{0}` `{0.id}`** | **Comando:** `{1.name}`\n**Servidor: `{2.name}`** `{2.id}` | **Canal: `#{3.name}`** `{3.id}`\n**Mensagem:** `{4.content}`".format(ctx.author, ctx.command, ctx.guild, ctx.channel, ctx.message))
        
        else:
            pass

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.author.id in self.bot.dono and ctx.command.is_on_cooldown(ctx):
            ctx.command.reset_cooldown(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        
    ################################################################################


        if re.search(r'discord(?:app\\?[\s\S]com\\?\/invite|\\?[\s\S]gg|\\?[\s\S]me)\/', message.content) or re.search(r'invite\\?[\s\S]gg\\?\/[\s\S]', message.content) or "privatepage" in message.content.lower() or "naked" in message.content.lower():
            if str("💼┃Parceiro") in [r.name for r in message.author.roles if r.name != "@everyone"] or str("772972507002568705") in [r.id for r in message.author.roles if r.name != "@everyone"]:
                print("OK")
                
            else:
                if not message.author.id in aviso1:
                    aviso1.append(message.author.id)
                    await message.delete()
                    embed=discord.Embed(description=f" <:unlike:760197986592096256> **|** Olá {message.author.mention}, não é permitido **CONVITES** de outros servidores sem a permissão dos **ADMINISTRADORES** segundo as regras.\nTendo isso em mente irei avisa-lo esse é seu **1° Strike**.\nNo **3° Strike** você será banido.", color=self.bot.cor)
                    msg = await message.channel.send(embed=embed)
                    await asyncio.sleep(10)
                    await msg.delete()
                elif not message.author.id in aviso2:
                    aviso2.append(message.author.id)
                    await message.delete()
                    embed=discord.Embed(description=f" <:unlike:760197986592096256> **|** Olá {message.author.mention}, não é permitido **CONVITES** de outros servidores sem a permissão dos **ADMINISTRADORES** segundo as regras.\nTendo isso em mente irei avisa-lo esse é seu **2° Strike**.\nNo **3° Strike** você será banido.", color=self.bot.cor)
                    msg = await message.channel.send(embed=embed)
                    await asyncio.sleep(10)
                    await msg.delete()
                else:
                    await message.delete()
                    aviso1.remove(message.author.id)     
                    aviso2.remove(message.author.id)       
                    print('ban')
                    #await message.author.send("pow pra que divulgar mano?\n\n~~não responda essa mensagem~~")
                    await message.author.ban(reason="Divulgando.")

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        if message.author.bot == False:
          if message.channel.id == 759814502798721024:
            return
          else:
            embed = discord.Embed(color=self.bot.cor)
            embed.set_author(name="Logs (Mensagem Apagada)", icon_url=message.author.avatar_url)
            if len(message.attachments) >= 1:
                link = message.attachments[0].url
                url = str(link).replace("https://cdn.discordapp.com/", "https://media.discordapp.net/")
                embed.set_image(url=url)
            else:
                pass
            if len(message.content) >= 1:
                embed.add_field(name="Mensagem", value=f"``{message.content[:900]}``", inline=True)
            else:
                pass
            embed.add_field(name="Usuário", value=f"``{message.author}`` - (<@{message.author.id}>)", inline=True)
            embed.add_field(name="Canal", value=f"``{message.channel.name}`` - (<#{message.channel.id}>)",
                                inline=True)
            timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
            time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))
            embed.add_field(name="Horário", value=f"``{time}``", inline=True)
            canal = message.guild.get_channel(self.bot.logs)
            if canal is None:
                return
            await canal.send(embed=embed)


    # ok
    @commands.Cog.listener()
    async def on_message_edit(self,before, after):
        
        if before.author.bot == False:
            if before.content != after.content:
                embed = discord.Embed(color=self.bot.cor)
                embed.set_author(name="Logs (Mensagem editada)", icon_url=before.author.avatar_url)
                if len(before.attachments) >= 1:
                    link = before.attachments[0].url
                    url = str(link).replace("https://cdn.discordapp.com/", "https://media.discordapp.net/")
                    embed.set_image(url=url)
                else:
                    pass
                if len(before.content) >= 1:
                    embed.add_field(name="Mensagem (Antes)", value=f"``{before.content[:900]}``", inline=True)
                    embed.add_field(name="Mensagem (Depois)", value=f"``{after.content[:900]}``", inline=True)

                else:
                    pass
                embed.add_field(name="Usuário:", value=f"``{before.author}`` - (<@{before.author.id}>)",
                                    inline=True)
                embed.add_field(name="Canal:", value=f"``{before.channel.name}`` - (<#{before.channel.id}>)",
                                    inline=True)

                timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
                time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))
                embed.add_field(name="Horário", value=f"``{time}``", inline=True)
                canal = before.guild.get_channel(self.bot.logs)
                if canal is None:
                    return
                await canal.send(embed=embed)
    '''
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, message_list):
        message_channel = message_list[0].channel
        nome = unidecode(message_channel.name).replace("|", "")
        filename = nome + "_as_" + datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%H_%M") + ".txt"
        headers = ["USUARIO", "ID", "Conteudo", "horario"]
        data = [[i.author.name + "#" + i.author.discriminator, i.author.id, i.content, i.created_at.strftime("%H:%M:%S - %d/%m/20%y")] for i in message_list]
        table = columnar(data, headers, no_borders=True, terminal_width=200)
        with open(filename, 'w+') as file:
            file.write(table)

        embed = discord.Embed(
            title='Messages Bulk Deleted',
            description=f'Messages bulk deleted from {message_channel.mention}. Deleted messages are available in the attached file.',
            color=self.bot.cor,
            timestamp=datetime.now(pytz.timezone('America/Sao_Paulo'))
        )
        channel = self.bot.get_channel(self.bot.logs)
        file = open(filename, 'r')
        await channel.send(embed=embed, file=discord.File(filename))
        file.close()
        #os.remove(filename)
        '''

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.bot: return
        if not self.bot.is_ready(): return
        if before.nick != after.nick:
            embed = discord.Embed(title='Nick alterado',
                                    colour=self.bot.cor,
                                    description=f'O(A) {after.name} mudou de nick!\n'
                                                f'User: {after.mention}\n'
                                                f'Id: {after.id}\n'
                                                f'Nick antigo: {before.nick}\n'
                                                f'Nick novo: {after.nick}',
                                    timestamp=datetime.utcnow())
            embed.set_thumbnail(url=str(after.avatar_url))
            channel = before.guild.get_channel(self.bot.logusers)
            await channel.send(embed=embed)
        if before.roles != after.roles:
                cargos = [f'<@&{c.id}>' for c in difference_between_lists(before.roles, after.roles)]
                # se a pessoa ficou com mais cargos, do que ela tinha antes
                if len(before.roles) < len(after.roles):
                    desc = None
                    if len(cargos) == 1:
                        desc = f'Novo cargo: {cargos[0]}'
                    elif len(cargos) > 1:
                        desc = 'Novos cargo: ' + ', '.join(cargos)
                else:  # se foi o contrário
                    desc = None
                    if len(cargos) == 1:
                        desc = f'Cargo removido: {cargos[0]}'
                    elif len(cargos) > 1:
                        desc = 'Cargos removidos: ' + ', '.join(cargos)
                embed = discord.Embed(title='Cargos alterados',
                                        colour=self.bot.cor,
                                        description=f'O(A) {after.name} sofreu alteração nos cargos!\n'
                                                    f'User: {after.mention}\n'
                                                    f'Id: {after.id}\n'
                                                    f'{desc}',
                                        timestamp=datetime.utcnow())
                embed.set_thumbnail(url=str(after.avatar_url))
                channel_cargos = self.bot.get_channel(self.bot.logscargos)
                await channel_cargos.send(embed=embed)
        if (before.premium_since is None) and (after.premium_since is not None):
                embed = discord.Embed(title='Novo booster',
                                        colour=self.bot.cor,
                                        description=f'O(A) {after.name} começou a dar boost!\n'
                                                    f'User: {after.mention}\n'
                                                    f'Id: {after.id}\n',
                                        timestamp=datetime.utcnow())
                embed.set_thumbnail(url=str(after.avatar_url))
                logsboost = self.bot.get_channel(772972566402826242)
                await logsboost.send(embed=embed)


    
    '''
    @commands.Cog.listener()  
    async def on_member_join(self, member):
      try:
        dev = member.guild.get_role(772972512711409725)
        await member.add_roles(dev)
      except:
        pass
        '''

def setup(bot):
    bot.add_cog(events(bot))
