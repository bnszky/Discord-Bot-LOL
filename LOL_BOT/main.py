import discord
import os
import json
from discord.ext import commands, tasks
import riot_request

TOKEN = os.environ.get('DISCORD_TOKEN')
REGION = 'eun1'
APIKEY = os.environ.get('RIOT_API_KEY')

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)

client = commands.Bot(command_prefix = '$', intents = intents)

def add_accounts(user, nick):
    with open('lol_accounts.json', 'r') as lol_ac:
        accounts = json.load(lol_ac)

    accounts[str(user.id)] = nick

    with open('lol_accounts.json', 'w') as lol_ac:
        json.dump(accounts, lol_ac)


@client.event
async def on_ready():
    print('LOL Bot is ready')

@client.event
async def on_member_join(member):
    add_accounts(member, None)

@client.command()
async def rank(ctx, nick = None):

    if nick == None:
        with open('lol_accounts.json', 'r') as lol_ac:
            accounts = json.load(lol_ac)
        nick = accounts[str(ctx.author.id)]

    if nick != None:
        await ctx.send(riot_request.rank_data(REGION, APIKEY, nick))
    else:
        await ctx.send('You must enter a nick')

@client.command()
async def rotation(ctx):
    await ctx.send('Free champions in this week: \n' + 
    riot_request.free_champions(APIKEY, REGION))

@client.command()
async def setnick(ctx, nick = None):
    add_accounts(ctx.author, nick)
    await ctx.send(f"{nick} account has been set up for {ctx.author.mention}")


client.run(TOKEN)