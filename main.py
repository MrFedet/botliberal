from io import BytesIO
import discord
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image, ImageChops, ImageDraw, ImageFont


load_dotenv()
TOKEN = "OTUwMDkzOTIxMTkzNzAxNDU2.YiT56g.kgUgR32FNCVi37V94uHNgLJxFbo"
client = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents().all())


def circle(pfp, size=(215, 215)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


@client.event
async def on_ready():
    print("Bot Activo")


@client.event
async def on_member_join(member):
    card = Image.open("card.png")

    asset = member.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = circle(pfp, (215, 215))
    card.paste(pfp, (425, 80))

    draw = ImageDraw.Draw(card)
    name = str(f"Bienvenido, {member.display_name}!")
    relleno = "                    Te uniste al \n" \
              "\t        Sindicato Liberal Libertario!"
    font = ImageFont.truetype("Montserrat-MediumItalic.ttf", 30)
    draw.text((365, 330), name, font=font, fill="white")
    draw.text((262, 380), relleno, font=font, fill="white")
    card.save("profile.png")
    await client.get_channel(950033328306790422).send(file=discord.File("profile.png"))
    await client.get_channel(950033328306790422).send("Ve al canal :rotating_light:**Roles** para seleccionar los roles!")


@client.command(pass_context=True)
async def autorole(ctx):
    embed = discord.Embed(
        title= "Bienvenidos al sindicato Liberal Libertario",
        description= "\n"
                     "🎥- Follower de MrFedet\n"
                     "💢- CS:GO\n"
                     "🔰- LOL\n"
                     "🏹- MINECRAFT\n"
                     "🍜- Otaku"
    )

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎥")
    await msg.add_reaction("💢")
    await msg.add_reaction("🔰")
    await msg.add_reaction("🏹")
    await msg.add_reaction("🍜")


@client.event
async def on_raw_reaction_add(payload):
    ourMessageID = 950435502383824988

    if ourMessageID == payload.message_id:
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == "🎥":
            role = discord.utils.get(guild.roles, name="Follower de MrFedet")
        elif emoji == "💢":
            role = discord.utils.get(guild.roles, name="CS:GO")
        elif emoji == "🔰":
            role = discord.utils.get(guild.roles, name="LOL")
        elif emoji == "🏹":
            role = discord.utils.get(guild.roles, name="Minecraft")
        elif emoji == "🍜":
            role = discord.utils.get(guild.roles, name="Otaku")
        await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    ourMessageID = 950435502383824988

    if ourMessageID == payload.message_id:
        guild = await (client.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        if emoji == "🎥":
            role = discord.utils.get(guild.roles, name="Follower de MrFedet")
        elif emoji == "💢":
            role = discord.utils.get(guild.roles, name="CS:GO")
        elif emoji == "🔰":
            role = discord.utils.get(guild.roles, name="LOL")
        elif emoji == "🏹":
            role = discord.utils.get(guild.roles, name="Minecraft")
        elif emoji == "🍜":
            role = discord.utils.get(guild.roles, name="Otaku")
        member = await (guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
            print("Memeber not found")


client.run(TOKEN)