import discord

from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Bot opérationnel.")

@bot.command(name='group')
async def showGroup(ctx):
    rolesUser = ctx.author.roles

    for role in rolesUser:
        if role.name == "TP A1":
            await ctx.channel.send("Hey")


bot.run("OTU2NTkyMTI1MDY2MjE5NjEw.Yjyd1w.BbkSPK1V55RxzTjUdCCZvsUVwXo")