import discord
from captcha.image import ImageCaptcha
from discord.ext import commands
from discord.ext.commands import Bot
from random import randint
import asyncio


class captchac(commands.Cog):
    def __init__(self,bot):
        self.bot = bot    
    
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        canal = discord.utils.get(member.guild.channels, name='「🔺」captcha')
        canal_boasvindas = discord.utils.get(member.guild.channels, name='「🚪」bem-vindo')
        await member.add_roles(member.guild.get_role(772972516817895484))
        await canal_boasvindas.send(f'{member.mention}, Seja bem vindo ao  nosso servidor, Leia as regras e seja feliz <3')
        try:
            numeros = randint(1000,10000)
            image = ImageCaptcha()
            data = image.generate('12345')
            send_img = image.write(str(numeros), 'out.png')
            mention = await canal.send(member.mention)
            embed = discord.Embed(description="",color=0x7289da)
            embed.set_author(name="🔑| Captcha")
            embed.add_field(name='Porfavor escreva os números a baixo (sem espaço) ',value= f"**--Tempo maximo de 5 minutos--**")
            embed.set_image(url="attachment://out.png")
            embed_enviado = await canal.send(embed=embed, file=discord.File('out.png'))

            check=lambda m: m.author == member            

            tentativas = 0
            tentativas_max = 2
            while tentativas <= tentativas_max:
                tentativas += 1
                msg = await self.bot.wait_for('message', check=check, timeout=300)
                if msg.content == str(numeros):
                    msg_sucesso = await canal.send('**Catpcha concluido com sucesso.**\n**Agora você se tornou um membro.**')
                    await member.remove_roles(member.guild.get_role(772972516817895484))
                    await member.add_roles(member.guild.get_role(772972512711409725)) 
                    await asyncio.sleep(10)
                    await mention.delete()
                    await msg_sucesso.delete()
                    await msg.delete()
                    await embed_enviado.delete()
                    break
                else:
                    if tentativas <= tentativas_max:
                        await canal.send(f'Resposta errada, você tem mais ``{tentativas_max - tentativas}`` tentativa(s)')
                    else:
                        await member.guild.kick(member, reason=f'{member} falhou durante o captcha.')

        except Exception as e:
            print(e)


def setup(bot):
  
    bot.add_cog(captchac(bot))