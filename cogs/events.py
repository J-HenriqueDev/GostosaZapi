import discord
import asyncio
from datetime import datetime
import pytz
import re
from discord.ext import commands
aviso1 = []
aviso2 = []
aviso3 = []

class events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self , guild, member):
        await asyncio.sleep(3)
        #moderator = 'Não encontrado.'
        #reason = "Não informada."
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
        #moderator = 'Não encontrado.'
        #reason = "Não informada."
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
        elif isinstance(error, commands.errors.CheckFailure):
          print("erro ao checar")
          pass
        elif isinstance(error, commands.CommandOnCooldown):
          m, s = divmod(error.retry_after, 60)
          return await ctx.send(f"**{ctx.author.name}**, aguarde **`{int(s)}`** segundo(s) para poder usar o comando **`{ctx.invoked_with}`** novamente.", delete_after=45)
        elif isinstance(error, commands.DisabledCommand):
          await ctx.send(f" <:unlike:760197986592096256> | **{ctx.author.name}**, o comando **`{ctx.invoked_with}`** está temporariamente desativado.")
        elif isinstance(error, commands.MissingRequiredArgument):
          await ctx.send('faltando argumentos')

    @commands.Cog.listener()
    async def on_member_join(self,member):
      if member.guild.id == 758823253825028167:
         dev = member.guild.get_role(759814435031875586)
         await member.add_roles(dev)

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot:
        return
        
      await self.bot.wait_until_ready()

      ctx = await self.bot.get_context(message)
      if message.content.replace('!', '') == ctx.me.mention:
          ctx.prefix = ctx.me.mention
          ctx.args = None
          ctx.author = message.author
      await self.bot.invoke(ctx)

  ##########################################################################   
      
      if message.channel.id == 759814496419708959:
          await message.add_reaction('<:like:760197986609004584>')
          return await message.add_reaction('<:unlike:760197986592096256>')


################################################################################


      if re.search(r'discord(?:app\\?[\s\S]com\\?\/invite|\\?[\s\S]gg|\\?[\s\S]me)\/', message.content) or re.search(r'invite\\?[\s\S]gg\\?\/[\s\S]', message.content) or "privatepage" in message.content.lower() or "naked" in message.content.lower():
        if str("</Link>") in [r.name for r in message.author.roles if r.name != "@everyone"] in [r.name for r in message.author.roles if r.name != "@everyone"]:
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
            await message.author.send("pow pra que divulgar mano?\n\n~~não responda essa mensagem~~")
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


def setup(bot):
    bot.add_cog(events(bot))
