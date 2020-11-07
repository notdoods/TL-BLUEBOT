from discord.ext import commands
from decouple import config
import asyncio

'''
FOR SURE NEED TO DO LIST:
EXTEND SO THAT I CAN CHANGE THE WIKI'S
'''
DISCORD_KEY = config('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='?')

@bot.command(name='gameslist')
async def gamesList(ctx):
    gl = open('gameslist.txt')
    lines = gl.readlines()
    gl.close()
    length = len(lines)//2
    A = lines[:length]
    B = lines[length:]
    page1 = ''.join(A)
    page2 = ''.join(B)
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

bot.load_extension('cogs.tournaments')
bot.run(DISCORD_KEY)