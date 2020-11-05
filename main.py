import discord
import os
import json
from config import secrets
from discord.ext import commands
from utils.role import emojis
from utils.role import cargos
from pymongo import MongoClient

intents = discord.Intents.all()
intents.members = True


class main(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(secrets.PREFIXO),

                        case_insensitive=True,
                        pm_help=None,
                        shard_count=1,
                        shard_ids=[0],
                        activity=discord.Activity(type=discord.ActivityType.watching, name='instagram.com/gostosazapi', status=discord.Status.do_not_disturb),
                        intents=intents)
        
        self.remove_command('help')
        self.cargo = cargos
        self._emojis = emojis
        self.dono = secrets.DONO
        self.adms = secrets.ADMS
        self.database = secrets.DATAB
        self.errado = "<:errado:761205727841746954>"
        self.correto = "<:correto:761205727670829058>"
        
        
        self.logsusers = 773567922526355496
        self.logscargos = 772998619304951810
        self.sugestao = 772972553769713735
        self.canais = ["772972558605090836","772972567308664882"]
        self.logs = 772972569326387232
        self.bans = 772972568655298574
        self.guild = 635624989193666591
        self.regras = 772972551713587210
        self.helper = 773518943490015233
        
        
        self.token = 'blz,talvez outro dia.'
        self.cor = 0xf10cdb
       
        self.carregados = 1
        self.falhas = 0
        for file in [c for c in os.listdir("cogs") if c.endswith(".py")]:
                name = file[:-3]
                try:
                    self.load_extension(f"cogs.{name}")
                    self.carregados += 1
                    print(f'MÓDULO [{file}] CARREGADO')
                except Exception as e:
                    print(f"FALHA AO CARREGAR  [{file}] MODULO ERROR [{e}]")
                    self.falhas += 1
        
    



    async def on_message(self, message):
        if message.guild is None:
          return 

        if message.author.bot or not message.channel.permissions_for(message.guild.me).send_messages:
          return
       
        ctx = await self.get_context(message)
       
        if not ctx.valid:
          return
       
        try:
            await self.invoke(ctx)
        except Exception as e:
            self.dispatch('command_error', ctx, e)

        if message.channel.id == self.sugestao:
            await message.add_reaction('<:like:760197986609004584>')
            return await message.add_reaction('<:unlike:760197986592096256>')


    async def on_ready(self):
        print('---------- Bot Online -----------')
        print(f"[OK] - {self.user.name} ({self.user.id}) - (Status - Online)")
        print(f"Modulos ativos: {len(bot.cogs)}")
        print(f'Usuários: {len(self.users) - len([c for c in self.users if c.bot])}')
        print(f'Bots: {len([c for c in self.users if c.bot])}')
        print(f'Guilds: {len(self.guilds)}')
        print('---------------------------------')

        log_ready = self.get_channel(679729322298441765)
        texto = f"<a:sabre:761230638044676106> **{self.user.name}** online | `{self.carregados}` Modulos Funcionando corretamente e `{self.falhas}` falhas detectadas."
        embed = discord.Embed(color=self.cor,description=texto)
        embed.set_author(name="BOT ONLINE",icon_url="https://media.discordapp.net/attachments/610244217763004430/760176340594065408/106913079_300540654602631_1385874962180230666_n.jpg")
        await log_ready.send(embed=embed)
       
        
        
bot = main()

if __name__ == '__main__':
    try:
        bot.run(secrets.TOKEN)
    except KeyboardInterrupt: 
        pass