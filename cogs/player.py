import aiohttp
import asyncio
from discord.ext import commands, tasks
import discord
from decouple import config
from datetime import date

API_KEY = config('API_KEY')
url = 'https://api.liquipedia.net/api'
tourneyURL = url + '/v1/team'

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = url + '/v1/player'

    @commands.command(name='searchplayer')
    async def searchplayer(self, ctx, wiki, id):
        pl = {'wiki': wiki.lower(), 'apikey': API_KEY, 'limit': 1, 'conditions': f'[[id::{id}]] OR [[pageid::{id}]]'}
        async with aiohttp.ClientSession() as cs:
            async with cs.post(self.url, data=pl) as r:
                response = await r.json()
                for result in response['result']:
                    payloadImage = {'wiki': wiki.lower(), 'apikey': API_KEY, 'limit': 1,
                                    'conditions': f'[[name::{result["team"]}]]'}
                    print(result)
                    e = discord.Embed(title=result['id'])
                    e.add_field(name='Full Name', value=result['name'], inline=False)
                    if result['romanizedname'] != '':
                        e.add_field(name='Romanized Name',value=result['romanizedname'],inline=False)
                    if result['localizedname'] != '':
                        e.add_field(name='Localized Name', value=result['localizedname'],inline=False)
                    e.add_field(name='Nationality', value=result['nationality'], inline=False)
                    if str(result['birthdate']) != '1000-01-01' or result['birthdate'] is result['deathdate']:
                        e.add_field(name='Birthday', value=str(result['birthdate']), inline=False)
                    else:
                        e.add_field(name='Birthday', value='????-??-??', inline=False)
                    earnings = format(result["earnings"], ",d")
                    e.add_field(name='Earnings', value='$' + str(earnings), inline=False)
                    e.add_field(name='Active?', value=result['status'],inline=False)
                    e.add_field(name='Team', value=result['team'], inline = False)

        async with aiohttp.ClientSession() as cs:
            async with cs.post(tourneyURL,data=payloadImage) as r:
                response = await r.json()
                for result in response['result']:
                    e.set_image(url=result['logourl'])
                    m = await ctx.send(embed=e)

    @commands.command(name='heplayers')
    async def highestearnedPlayer(self, ctx, wiki):
        d = date.today().strftime("%Y-%m-%d")
        #Create pages using Reactions, limit:100, and keeping track
        #Basic logic from my understanding:
        #Bot will add reactions for left and right arrows, if the user reacts w/ the error, edit the message and remove their reaction.
        pl = {'wiki': wiki, 'apikey': API_KEY, 'limit': 100,'order':'earnings DESC'}
        initial = await ctx.send(f'The highest earned teams for {wiki}: ')
        async with aiohttp.ClientSession() as cs:
            async with cs.post(self.url, data=pl) as r:
                response = await r.json()
                maxpagenumber = 10
                current = 1
                allContent = []
                count = 1
                message = ''
                for result in response['result']:
                    earnings = format(result["earnings"], ",d")
                    message += f'[{result["pageid"]}]  ' '**'+ result["id"] +f'**\n*${str(earnings)}* ' + '\n'
                    count += 1
                    if count%maxpagenumber == 0:
                        allContent.append(message)
                        message = ''
                m = await ctx.send(f">>> **Page {current}/{maxpagenumber}**: \n\n {allContent[current-1]}")

                await m.add_reaction("◀")
                await m.add_reaction("▶")

                def check(reaction,user):
                    return user == ctx.author and str(reaction.emoji) in ["◀","▶"]

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
                        if str(reaction.emoji) == "▶" and current != maxpagenumber:
                            current += 1
                            await m.edit(content=f">>> **Page {current}/{maxpagenumber}**: \n\n{allContent[current-1]}")
                            await m.remove_reaction(reaction,user)

                        elif str(reaction.emoji) == "◀" and current > 1:
                            current -= 1
                            await m.edit(content=f">>> **Page {current}/{maxpagenumber}**: \n\n{allContent[current - 1]}")
                            await m.remove_reaction(reaction, user)
                        else:
                            await m.remove_reaction(reaction,user)
                    except asyncio.TimeoutError:
                        await m.delete()
                        await initial.delete()
                        break

def setup(bot):
    bot.add_cog(Player(bot))