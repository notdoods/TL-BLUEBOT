import aiohttp
import asyncio
from discord.ext import commands, tasks
import discord
from decouple import config
from datetime import date


API_KEY = config('API_KEY')
url = 'https://api.liquipedia.net/api'
playerURL = url + '/v1/player'

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = url + '/v1/team'

    @commands.command(name='searchteam')
    async def searchteam(self, ctx, wiki, id):
        pl = {'wiki': wiki.lower(), 'apikey': API_KEY, 'limit': 1, 'conditions':f'[[name::{id}]] OR [[pageid::{id}]]'}
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.post(self.url, data=pl) as r:
                    response = await r.json()
                    if response['result'] != []:
                        for result in response['result']:
                            plplayers = {'wiki': wiki.lower(), 'apikey': API_KEY, 'limit': 20,
                                            'conditions': f'[[team::{result["name"]}]] AND [[status::Active]]'}
                            e = discord.Embed(title=result['name'], url=result['links']['website'])
                            e.set_image(url=result['logourl'])
                            e.set_thumbnail(url=result['logourl'])
                            e.add_field(name='Location', value=result['location'], inline=False)
                            if str(result['createdate']) != '1000-01-01':
                                e.add_field(name='Create Date', value=str(result['createdate']), inline=False)
                            else:
                                e.add_field(name='Create Date', value='????-??-??',inline=False)
                            earnings = format(result["earnings"], ",d")
                            e.add_field(name='Earnings', value='$' + str(earnings), inline=False)
                            e.add_field(name='Coach', value=result['coach'], inline=False)
                    else:
                        raise Exception()

            async with aiohttp.ClientSession() as cs:
                async with cs.post(playerURL,data=plplayers) as r:
                    response = await r.json()
                    playerlist = ''
                    for result in response['result']:
                        playerlist += f'[{result["pageid"]}]  {result["id"]}\n'
                    e.add_field(name='Active Players', value=playerlist, inline=False)
                    await ctx.send(embed=e)
        except:
            await ctx.send('Error finding team: Make sure ID is valid/name is EXACT match (proper capitalization for the organization)')


    @commands.command(name='heteams')
    async def highestearnedTeams(self, ctx, wiki):
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
                    message += f'[{result["pageid"]}]  ' '**'+ result["name"] +f'**\n*${str(earnings)}* ' + '\n'
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
    bot.add_cog(Teams(bot))