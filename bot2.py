# bot.py
import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import datetime
import time as t
import helpers

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        try:
            bdays_file = open(str(guild.id) + "birthdays.txt", mode="r")
        except FileNotFoundError:
            bdays_file = open(str(guild.id) + "birthdays.txt", mode="w")
            bdays_file.write("user,bday\n")
            bdays_file.close()
            print(f"Bday file not found for {guild.name}, creating...")
        try:
            chan_file = open(str(guild.id) + "channel.txt", mode="r")
        except FileNotFoundError:
            chan_file = open(str(guild.id) + "channel.txt", mode="w")
            chan = guild.system_channel
            chan_file.write(str(chan.id))
            chan_file.close()
            print(f"Chan file not found for {guild.name}, creating...")
    
@bot.event
async def on_guild_join(guild):
    bdays_file = open(str(guild.id) + "birthdays.txt", mode="w")
    bdays_file.write("user,bday\n")
    bdays_file.close()
    chan_file = open(str(guild.id) + "channel.txt", mode="w")
    chan = guild.system_channel
    chan_file.write(str(chan.id))
    chan_file.close()
    await guild.system_channel.send("Thank you for using Birthday Bot.\nPlease use the command `!change-channel` to set the default output channel for this bot, otherwise this channel will be the default output channel.\nOnce this is done, use `!add-birthday` to add your birthday to the list!")

@bot.event
async def on_guild_remove(guild):
    try:
        os.remove(str(guild.id) + "birthdays.txt")
        os.remove(str(guild.id) + "channel.txt")
    except FileNotFoundError:
        return
    
@tasks.loop(hours=1.0, reconnect=False)
async def check_bdays():
    print("Checking birthdays")
    print(datetime.datetime.now().hour)
    if datetime.datetime.now().hour == 9:
        print("Birthday found")
        await helpers.check_bdays(bot)

@check_bdays.before_loop
async def before_check_bdays():
    print('waiting...')
    await bot.wait_until_ready()

@bot.command(name='add-birthday', help='Use this to add your birthday in the format YYYY-MM-DD.')
async def add_birthday(ctx, bday):
    if not helpers.validate_bday(bday):
        await ctx.send("Please enter your birthday in the format YYYY-MM-DD.")
        return
    await helpers.add_bday(ctx, bday)
    
@bot.command(name='change-birthday', help='Use this to change your currently saved birthday.')
async def change_birthday(ctx, bday):
    if not helpers.validate_bday(bday):
        await ctx.send("Please enter your birthday in the format YYYY-MM-DD.")
        return
    await helpers.change_bday(ctx, bday)

@bot.command(name='change-channel', help='Use this to change the output channel for the bot.')
async def change_channel(ctx, chan):
    await helpers.change_channel(ctx, chan)

@bot.command(name='list-birthdays', help='Use this to list every birthday currently stored for the server.')
async def list_birthdays(ctx):
    await helpers.list_bdays(ctx)

check_bdays.start()

bot.run(TOKEN)