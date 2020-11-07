# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import aiohttp
import asyncio
from discord.ext import commands, tasks
import discord
from decouple import config
from datetime import date


API_KEY = config('API_KEY')
url = 'https://api.liquipedia.net/api'

'''
THIS IS THE TOURNAMENT SECTION
HAS 3 BASICS FUNCTIONS
[?searchtourney] This takes the pageid of a tournament and displays relevant information from the API
[?upcoming] This displays the next 10 tournaments coming up from specified game
[?recenttourneys] This displays pages of recent tournaments, which the user can control which page they are on via reactions.
'''
class Tournaments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = url + '/v1/tournament'

    @commands.command(name='searchtourney')
    async def tourney(self, ctx, wiki, id):
        pl = {'wiki': wiki, 'apikey': API_KEY, 'limit': 1, 'conditions': f'[[pageid::{id}]]','order':'name ASC, startdate DESC'}
        async with aiohttp.ClientSession() as cs:
            async with cs.post(self.url , data=pl) as r:
                response = await r.json()
                for result in response['result']:
                    print(result)
                    e = discord.Embed(title=result['name'])
                    e.set_image(url=result['bannerurl'])
                    e.set_thumbnail(url=result['iconurl'])
                    #Change this to instead insert new fields
                    e.add_field(name='Start Date', value=result['startdate'], inline=False)
                    e.add_field(name='Prize Pool', value='$'+str(result['prizepool']),inline=False)
                    e.add_field(name='# of Participants/Teams', value=result['participantsnumber'],inline=False)
                    e.add_field(name='Location', value=result['location'],inline=False)
                    e.set_footer(text=f'Patch version: {result["patch"]}')
                    if 'winner' in result['extradata'].keys():
                        if result['extradata']['winner'] != 'tbd':
                            e.add_field(name='Winners', value=result['extradata']['winner'].title(),inline=False)
                            e.add_field(name='Runner Up', value=result['extradata']['runnerup'].title(),inline=False)
                        else:
                            e.add_field(name='Winners',value='TBD',inline=False)
                    else:
                        e.add_field(name='Winners', value='TBD', inline=False)
                    await ctx.send(embed=e)

    @commands.command(name='upcoming')
    async def upcoming(self, ctx, wiki):
        d = date.today().strftime("%Y-%m-%d")
        pl = {'wiki': wiki, 'apikey': API_KEY, 'limit': 10, 'conditions': f'[[startdate::>{d}]]','order':'startdate ASC'}
        await ctx.send(f'The following upcoming tournaments for {wiki}: ')
        message = '>>> ***SearchID/Name***\n'
        async with aiohttp.ClientSession() as cs:
            async with cs.post(self.url, data=pl) as r:
                response = await r.json()
                for result in response['result']:
                    message += f'[{result["pageid"]}]  ' '**'+ result["name"] +f'**\n*{result["startdate"]}* ' + '\n'
                await ctx.send(message)

    @commands.command(name='recenttourneys')
    async def recent(self, ctx, wiki):
        d = date.today().strftime("%Y-%m-%d")
        #Create pages using Reactions, limit:100, and keeping track
        #Basic logic from my understanding:
        #Bot will add reactions for left and right arrows, if the user reacts w/ the error, edit the message and remove their reaction.
        pl = {'wiki': wiki, 'apikey': API_KEY, 'limit': 100, 'conditions': f'[[startdate::<{d}]]','order':'startdate DESC'}
        initial = await ctx.send(f'The following upcoming tournaments for {wiki}: ')
        async with aiohttp.ClientSession() as cs:
            async with cs.post(self.url, data=pl) as r:
                response = await r.json()
                maxpagenumber = 10
                current = 1
                allContent = []
                count = 1
                message = ''
                for result in response['result']:
                    message += f'[{result["pageid"]}]  ' '**'+ result["name"] +f'**\n*{result["startdate"]}* ' + '\n'
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




'''
This is a way to get players of a certain team that are currently active
Important things to note that I just learned:

When doing something like if a name contains, use [[name::>____]], proper capitalization

pl = {'wiki':'dota2', 'apikey':API_KEY, 'limit':10, 'conditions':'[[pagename::Beastcoast]] AND [[extradata_leavedate::]] AND [[name::>Wisp]]'}
datapoint_url = url + '/v1/datapoint'
@bot.command(name='test2')
async def testDatapoint(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.post(datapoint_url, data=pl) as r:
            response = await r.json()
            for r in response['result']:
                print(r)
'''
def setup(bot):
    bot.add_cog(Tournaments(bot))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
