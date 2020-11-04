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
        print("( * ) | Tentando se conectar ao banco de dados...")
        try:
            mongo = MongoClient(self.database)
        except Exception as e:
            print(f"\n<---------------->\n( ! ) | Erro na tentativa de conexão com o banco de dados!\n<----------->\n{e}\n<---------------->\n")
            exit()
    
        self.db = mongo['bard']
        print(f"( > ) | Conectado ao banco de dados!")
    
    
    def formatPrefix(self, ctx):
        prefix = ctx.prefix if not str(self.user.id) in ctx.prefix else f'@{ctx.me} '
        return ctx.prefix.replace(ctx.prefix, prefix)

    # Embeds
    """
    def embed(self, ctx, invisible=False):
        color = self.neutral if invisible else self.cor
        emb = discord.Embed(color=color)
        emb.set_footer(text=self.user.name + " © 2020", icon_url=self.user.avatar_url_as())
        emb.timestamp = ctx.message.created_at
        return emb
    """

    async def on_message(self, message):
        return

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

@bot.check
async def blacklist(ctx):
    with open('cogs/utils/users_banned.json') as bn:
        jsn = json.load(bn)
    if str(ctx.author.id) in jsn and not ctx.author.id == bot.dono:
        reason = jsn[str(ctx.author.id)]
        embed = discord.Embed(title=f'<:unlike:760197986592096256> | Sem permissão!', description=f'Você foi banido de usar qualquer comando meu, o motivo é:\n`{reason}`', color=bot.ecolor)
        await ctx.send(embed=embed)
        return False
    return True

if __name__ == '__main__':
    try:
        bot.run(secrets.TOKEN)
    except KeyboardInterrupt: 
        pass