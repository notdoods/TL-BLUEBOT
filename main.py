from discord.ext import commands
import discord
from decouple import config
import asyncio


'''
FOR SURE NEED TO DO LIST:
EXTEND SO THAT I CAN CHANGE THE WIKI'S
'''
DISCORD_KEY = config('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='?')
q = config('q')
@bot.command(name='gameslist')
async def gamesList(ctx):
    gl = open('gameslist.txt')
    lines = gl.readlines()
    gl.close()
    length = len(lines)//2
    page1 = ''.join(lines[:length])
    page2 = ''.join(lines[length:])
    allPages = [page1,page2]
    current = 1
    maxpagenumber = 2
    m = await ctx.send(f">>> **Page {current}/{maxpagenumber}**: \n\n {allPages[current - 1]}")

    await m.add_reaction("◀")
    await m.add_reaction("▶")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀", "▶"]

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)
            if str(reaction.emoji) == "▶" and current != maxpagenumber:
                current += 1
                await m.edit(content=f">>> **Page {current}/{maxpagenumber}**: \n\n{allPages[current - 1]}")
                await m.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀" and current > 1:
                current -= 1
                await m.edit(content=f">>> **Page {current}/{maxpagenumber}**: \n\n{allPages[current - 1]}")
                await m.remove_reaction(reaction, user)
            else:
                await m.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await m.delete()
            break

API_KEY = config('API_KEY')
url = 'https://api.liquipedia.net/api/v1/match'

@bot.command(name='q')
async def Q(ctx):
    e = discord.Embed(title='Q')
    e.set_image(url=q)
    await ctx.send(q)

bot.load_extension('cogs.player')
bot.load_extension('cogs.tournaments')
bot.load_extension('cogs.teams')
bot.run(DISCORD_KEY)