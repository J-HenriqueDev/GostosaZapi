import discord
import os
import json
from config import secrets
from discord.ext import commands
from utils.role import emojis





class main(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(secrets.PREFIXO),
                         case_insensitive=True,
                         pm_help=None)
        
        self._emojis = emojis
        self.dono = secrets.DONO
        self.adms = secrets.ADMS
        self.errado = "<:errado:761205727841746954>"
        self.correto = "<:correto:761205727670829058>"
        self.canais = ["759814502798721024","759814507336826880"]
        self.logs = 759814509287440427
        self.bans = 759814509287440427
        self.guild = 758823253825028167
        self.token = 'blz,talvez outro dia.'
        self.cor = 0xf10cdb
        self.ecolor = 0xDD2E44
        self.neutral = 0x36393F
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

    
    
    def formatPrefix(self, ctx):
        prefix = ctx.prefix if not str(self.user.id) in ctx.prefix else f'@{ctx.me} '
        return ctx.prefix.replace(ctx.prefix, prefix)

    # Embeds
    def embed(self, ctx, invisible=False):
        color = self.neutral if invisible else self.cor
        emb = discord.Embed(color=color)
        emb.set_footer(text=self.user.name + " © 2020", icon_url=self.user.avatar_url_as())
        emb.timestamp = ctx.message.created_at
        return emb

    def erEmbed(self, ctx, error='Erro!'):
        emb = discord.Embed(title=f'<:unlike:760197986592096256> | {error}', color=self.ecolor)
        emb.set_footer(text=f'Executado por {ctx.author.name}', icon_url=ctx.author.avatar_url)
        emb.timestamp = ctx.message.created_at
        return emb

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
