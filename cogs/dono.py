from discord.ext import commands
import asyncio
from contextlib import redirect_stdout
import inspect
import discord
import json
from io import StringIO
import traceback
import textwrap
import time
import sys

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def debug(self, ctx, *, args=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if args is None:
            embed = discord.Embed(description="**|** Olá {}, você não inseriu uma variável".format(ctx.author.mention),
                                  color=self.bot.cor)
            await ctx.send(embed=embed)
            return


        args = args.strip('` ')
        python = '```py\n{}\n```'
        result = None
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'msg': ctx.message,
        }
        env.update(globals())
        try:
            result = eval(args, env)
            if inspect.isawaitable(result):
                result = await result
            embed = discord.Embed(colour=self.bot.cor)
            embed.add_field(name="Entrada", value='```py\n{}```'.format(args), inline=True)
            embed.add_field(name="Saida", value=python.format(result), inline=True)
            embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
            print(f"DEGUG USADO POR : {ctx.author}")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(colour=self.bot.cor)
            embed.add_field(name="Entrada", value='```py\n{}```'.format(args), inline=True)
            embed.add_field(name="Saida", value=python.format(type(e).__name__ + ': ' + str(e)), inline=True)
            embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
            await ctx.send(embed=embed)
            print(f"DEGUG USADO POR : {ctx.author}")
            return
            
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def reload(self, ctx, *, cog: str = None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if cog is None:
            return await ctx.send(f"{ctx.author.mention} Não foi inserido a cog para recarregar!", delete_after=15)
        await ctx.message.delete()
        if not cog in self.bot.cogs:
            cog_list = ",".join([c for c in self.bot.cogs])
            await ctx.send(f"{ctx.author.mention} **Módulo  invalido. Módulos disponiveis abaixo**\n```python\n{cog_list}\n```", delete_after=15)
            return
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            embed = discord.Embed(
                colour=self.bot.cor,
                description=(f"**[Sucesso] O Modulo `{cog}` foi recarregado corretamente!**"))

            await ctx.send(embed=embed, delete_after=20)
        except Exception as e:
            embed = discord.Embed(
                colour=self.bot.cor,
                description=(f"**[ERRO] O Modulo `{cog}` não foi recarregado corretamente**\n\n``{e}``"))

            await ctx.send(embed=embed, delete_after=20)
            print(f"RELOAD USADO POR : {ctx.author}")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def reiniciar(self,ctx):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        import os
        import sys
        await ctx.message.delete()
        embed = discord.Embed(description=f"<:like:760197986609004584> O **{ctx.me.name}** está sendo reiniciado!", color=self.bot.cor)
        await ctx.send(embed=embed)
        print(f"REINICIAR USADO POR : {ctx.author}")
        def reiniciar_code():
           python = sys.executable
           os.execl(python, python, * sys.argv)
        print('Reiniciando...')
        reiniciar_code()


    @commands.command(
        name='desativarcomando',
        aliases=['dcmd','acmd','ativarcomando'],
        description='desativa um comando do bot',
        usage='c.desativarcomando <Nome do Comando>'
    )
    async def _desativarcomando(self, ctx, *, nome=None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        if nome is None:
            return await ctx.send(f"{ctx.author.mention} você não inseriu um comando pra desativar.", delete_after=20)
       
        comando = self.bot.get_command(nome)
        if not comando:
            return await ctx.send(f"<:incorreto:594222819064283161> | **{ctx.author.name}**, não encontrei nenhum comando chamado **`{nome}`**.")

        if comando.enabled:
            comando.enabled = False
            await ctx.send(f"<:unlike:760197986592096256>**{ctx.author.name}**, você desativou o comando **`{comando.name}`**.")
        else:
            comando.enabled = True
            await ctx.send(f"<:like:760197986609004584> **{ctx.author.name}**, você ativou o comando **`{comando.name}`**.")


    @commands.command(hidden=True)
    async def exec(self, ctx, *, body: str):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return
        def clean(content):
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])
            return content.strip('` \n')

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'msg': ctx.message,
        }

        env.update(globals())

        body = clean(body)
        stdout = StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "    ")}' # 4 espaços = tab, se quiser tab mesmo coloque \t dentro do ""

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()

        except:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')


    @commands.command()
    async def roleall(self, ctx,*, rola :discord.Role =  None):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return      
        membros_total = 1 
        if rola is None:
            return await ctx.send("argumentos")
        else:
            #cargo = ctx.guild.get_role(rola)
            await ctx.send("<a:run_child:763119754881794068> Procurando na lista de cargos...",delete_after=5)
            #await asyncio.sleep(5)
            await ctx.send(f"<a:Checkmark:763111771611201546> o cargo **{rola.name}** foi encontrado.")
            #await asyncio.sleep(5)
            await ctx.send("<a:WideTrump:763119810279374898> Iniciando o processo de adição em massa de cargos.")
            try:
                for member in ctx.guild.members:
                    tst = [c.id for c in member.roles]
                    if rola.id in tst:
                        pass
                    elif member.bot:
                        pass
                    else:
                        await self.bot.loop.create_task(member.add_roles(rola))
                        membros_total += 1
                        await ctx.channel.send(f"<a:Checkmark:763111771611201546> **{member}** recebeu o cargo ``{rola.name}``.")
                
                if membros_total == 1:
                    await ctx.send(f"{self.bot._emojis['incorreto']} Todos os membros já possuem o cargo ``{rola.name}``")
                else:
                    await ctx.send(f"<a:FuckMeBabe:763119842215329813> {membros_total} membros receberam o cargo ``{rola.name}``.")
            except Exception as e:
                print(e)
    
    @commands.command()
    async def check(self, ctx):
        if not str(ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
          await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
          return   
        cargo = ctx.guild.get_role(759814435031875586)
        try:
            for member in ctx.guild.members:
                if member.bot:
                    pass
                else:
                    await self.bot.loop.create_task(member.add_roles(cargo))
        except Exception as e:
            print(e)
            
  


def setup(bot):
    bot.add_cog(Owner(bot))
