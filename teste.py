from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps


avatar = Image.open("cogs/img/avatar.png")
avatar = avatar.resize((210, 210));
bigsize = (avatar.size[0] * 2,  avatar.size[1] * 2)
mask = Image.new('L', bigsize, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + bigsize, fill=255)
mask = mask.resize(avatar.size, Image.ANTIALIAS)
avatar.putalpha(mask)

saida = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
saida.putalpha(mask)

fundo = Image.open('cogs/img/bem-vindo.png')
fonte = ImageFont.truetype('cogs/img/college.ttf',42)
escrever = ImageDraw.Draw(fundo)
escrever.text(xy=(230,345), text="BUCETACARUNUDA#1234",fill=(0,0,0),font=fonte)

fundo.paste(saida, (357, 39), saida)
fundo.save("cogs/img/teste.png")   