import discord
from asyncio import TimeoutError as Esgotado   
from captcha.image import ImageCaptcha
from discord.ext import commands
from discord.ext.commands import Bot
from random import randint
import asyncio

class captcha(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.formulario = []
  
    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild.id == self.bot.guild and not member.bot:
            canal = discord.utils.get(member.guild.channels, name='「」captcha')
            canal_boasvindas = discord.utils.get(member.guild.channels, name='「」bem-vindo')
            await member.add_roles(member.guild.get_role(772972516817895484))
            await canal_boasvindas.send(f'{member.mention}, seja bem vindo ao ``{member.guild.name}``, leia as <#{self.bot.regras}> e seja feliz <3')
            try:
                numeros = randint(1000,10000)
                image = ImageCaptcha()
                data = image.generate('12345')
                send_img = image.write(str(numeros), 'out.png')
                mention = await canal.send(member.mention)
                self.formulario.append(member.id)
                embed = discord.Embed(description="",color=0x7289da)
                embed.set_author(name="🔑| Captcha")
                embed.add_field(name='Por favor escreva os números abaixo (sem espaço)',value= f"**--Tempo máximo de 5 minutos--**")
                embed.set_image(url="attachment://out.png")
                embed_enviado = await canal.send(embed=embed, file=discord.File('out.png'))

                check=lambda m: m.author == member


                captcha = None
                while captcha is None:
                    try:
                        resposta = await self.bot.wait_for("message", check=check, timeout=300)
                    except Esgotado:
                        await canal.send(f"**{member.name}**, você demorou muito para fornecer o captcha,então voçê será kickado!", delete_after=30)
                        await member.kick()
                        await embed_enviado.delete()
                        break
                    if tentativas == 3:
                        await canal.send(f"**{member.name}**, você errou o captcha 5 vezes então será kickado!", delete_after=20)
                        self.formulario.remove(member.id)
                        await member.kick()
                        await embed_enviado.delete()
                        break
                    elif resposta.content == str(numeros):
                        await canal.send('**Catpcha concluido com sucesso.**\n**Agora você se tornou um membro.**')
                        await member.remove_roles(member.guild.get_role(772972516817895484))
                        await member.add_roles(member.guild.get_role(772972512711409725)) 
                        await asyncio.sleep(3)
                        await embed_enviado.delete()
                    
                    elif not resposta.content == str(numeros):
                        tentativas += 1
                        await canal.send(f"**Você errou o captcha pqp otário**\nTentativa: `{tentativas}/3`", delete_after=60)
                    else:
                        nome = resposta.content        
 
                if not nome:
                    return self.formulario.remove(member.id)

                await canal.send('**Catpcha concluido com sucesso.**\n**Agora você se tornou um membro.**')
                await member.remove_roles(member.guild.get_role(652223688988426270))
                await member.add_roles(member.guild.get_role(647720763217936394))
                await embed_enviado.delete()

            except Exception as e:
                print(e)


def setup(bot):
    bot.add_cog(captcha(bot))