import discord
from discord.ext import commands
import config
from twitter import *

#Discord API
discordToken = config.discord["key"]
bot = discord.Client()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='Gets the most recent tweet from a designated user.')
#Twitter API
twitter = Twitter(auth = OAuth(
    config.twitter['access_token'],
    config.twitter['access_secret'],
    config.twitter['consumer_key'],
    config.twitter['consumer_secret']
))

#Variables
uHandle = "Twitter"

def latest_tweet(target_handle):
    responses = twitter.statuses.user_timeline(screen_name = target_handle)
    return responses[0]['text']

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, "You are missing a parameter.")
    raise error;

@bot.command(pass_context = True)
async def tweet(ctx):
    await bot.send_message(ctx.message.channel, uHandle + ": " + latest_tweet(uHandle))
@bot.command(pass_context = True)
async def handle(ctx, userhandle:str):
    global uHandle
    uHandle = userhandle
    await bot.send_message(ctx.message.channel, "User Handle Set To: " + userhandle)

bot.run(discordToken)