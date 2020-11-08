TL BLUEBOT is a Discord Bot that brings esports information from Liquipedia straight to your Discord channel! 
This bot includes commands that displays tournaments, matches, teams, and players information. We decided to make this project since almost everyone uses Discord (as it was even required to have to participate in this hackathon!) and would help encourage engagement in esports discussion with proper information with ease of access. Ultimately, we want to bring esports to a bigger light and help create, in essence, longevity of the industry.

Check out the link for the discord bot at 

https://ellertson.org/projects/tlbluebot/

### This project was made by
* Kevin Chao (App Developer)
* Parker Ellertson (Website Backend Developer)
* Coby Moore (Graphic Designer)

#### This project was made with
* Python
* Discord API
* Liquipedia DB API
* HTML/CSS

The following segments will show you the commands that are available in this build of TL BLUEBOT

### NOTE! All inputs are cap sensitive! This is necessary for accurate listings
## Setup/Start
To add the bot, check out the link at the top of this README and hit the add bot link

The bot uses the command prefix to operate: ? 

After adding the bot, you can check out what games are available for search via:
```
?gameslist 
```
which will create a list of games in the format:
```
[gamename] as [gameID]
```

## Tournament
With the gameID of specified game, you can now start using it to access information from the commands from here on out. Here is a list of the commands w/ their input for tournament:

```
?upcoming [gameID]
?recenttourneys [gameID]
?tourney [gameID] [tournamentID]
?searchseries [gameID] "[Series Name]"
```
Both ?upcoming and ?recenttourneys will display in the format:

[tournamentID] Tournament Name, Date

?upcoming  provides the next 10 upcoming tournaments for specified game, sorted from closest to furthest date. An example of this would be 
```
?upcoming dota2
```
?recenttourneys provides the most recent tournament for specified game, sorted from closest to furthest date, up to 100 total tournaments. The user will be presented with 10 entries initially and can click the arrows provided to go to the next 10 entries. An example of this would be 
```
?recenttourneys dota2
```
?searchtourneys provides the specified tournament's information, including Series name, start date, prize pool, # of participants/teams, location, the winners, and placements! As a reminder, ?upcoming and ?recenttourneys results can get [tournamentID]. An example of searchtourneys would look like
```
?searchtourneys dota2 25049
```
?searchseries will give a list of tournaments that are considered to be of the same series, up to 100 tournaments. Using the example for searchtourneys, that would give result in information about "The International 2015", with the series name being "The International". An example of ?searchseries is given

```
?searchseries dota2 "The International"
```
Note the quotations and capitalizations in "The International", this is necessary to provide an accurate listing.

## Matches
These are the commands to look at specific matches of a tournament
```
?searchmatches [gameID] [Tournament Name]
?match [gameID] [matchID]
```
?searchmatches will give a list of matches to view (up to 100 entries) from specified tournament, sorted from the newest matches. The format of the results will be as such, along with an example
```
[matchID] Match Name, Final Score
?searchmatches dota2 "The International 2015"
```
Note: The search is capitalization sensitive for accurate listings.

?match will give links to the VOD for each game played, the final score, and the team roster at the time. An example of usage would be
```
?match dota2 6240273
```
## Teams
The following commands for teams is
```
?heteams [gameID]
?team [gameID] [teamID OR Team Name]
```

?heteams , meaning "Highest Earning Teams", provides a list of the highest earning teams for specified game, with the format being 
```
[teamID] Team Name, Total Earnings in $
```
?team searches the team for specified game, giving details such as Team's location, create date, total earnings, the coach, logo, and the active players and their playerID. Example of usage is below
```
?team dota2 35854
?team dota2 OG
```
Both examples will provide the same team, team OG for Dota 2.
## Players
Just like Teams, there are two similar commands
```
?heplayers [gameID]
?player [gameID] [playerID OR Player Name]
```

?heplayers provides a list of the highest earning player for specified game in the format of 
```
[playerID] Player Name, Total Earnings
```

?player details information about the specified player in specified game. The information includes full name, nationality, birthday, total earnings, if they are active, and the current team. The input for this is

```
?player dota2 2980
?player dota2 N0tail
```
Both of these examples would give the result of the player, N0tail . 
