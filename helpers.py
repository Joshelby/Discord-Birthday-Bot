import datetime
import csv
import discord

def validate_bday(bday):
    try:
        datetime.date.fromisoformat(bday)
    except ValueError:
        return False
    return True

async def add_bday(ctx, bday):
    bdays_file = open(str(ctx.guild.id) + "birthdays.txt", mode="r")
    csv_reader = csv.DictReader(bdays_file, ["user", "bday"])
    for row in csv_reader:
        if row["user"] == str(ctx.author.id):
            await ctx.send(f"You already have a birthday stored of {row['bday']}.\nPlease use the change-birthday command if this is incorrect.")
            return
    bdays_file.close()
    bdays_file = open(str(ctx.guild.id) + "birthdays.txt", mode="a")
    csv_writer = csv.DictWriter(bdays_file, ["user", "bday"])
    csv_writer.writerow({"user": ctx.author.id, "bday": bday})
    bdays_file.close()
    await ctx.send(f"Birthday for {ctx.author.display_name} added successfully!")

async def change_bday(ctx, bday):
    bdays_file = open(str(ctx.guild.id) + "birthdays.txt", mode="r")
    csv_reader = csv.DictReader(bdays_file, ["user", "bday"])
    temp_bdays_dict = {}
    for row in csv_reader:
        if row["user"] == str(ctx.author.id):
            row["bday"] = bday
        temp_bdays_dict[row["user"]] = row["bday"]
    print(temp_bdays_dict)
    bdays_file.close()
    bdays_file = open(str(ctx.guild.id) + "birthdays.txt", mode="w")
    csv_writer = csv.DictWriter(bdays_file, ["user", "bday"])
    for item in temp_bdays_dict.items():
        csv_writer.writerow({"user": item[0], "bday": item[1]})
    bdays_file.close()
    await ctx.send(f"Birthday for {ctx.author.display_name} updated successfully!")

async def change_channel(ctx, chan):
    channel = discord.utils.get(ctx.guild.text_channels, name=chan)
    if channel == None:
        await ctx.channel.send("That channel does not appear to exist, please try again.")
        return
    chan_file = open(str(ctx.guild.id) + "channel.txt", mode="w")
    chan_file.write(str(channel.id))
    chan_file.close()
    await ctx.channel.send(f"Output channel successfully changed to {channel.name}.")

async def check_bdays(bot):
    for guild in bot.guilds:
        print(guild.name)
        bdays_file = open(str(guild.id) + "birthdays.txt", mode="r")
        csv_reader = csv.DictReader(bdays_file, ["user", "bday"])
        todays_date = datetime.date.today()
        for row in csv_reader:
            if row["user"] == "user":
                continue
            cur_bday = datetime.date.fromisoformat(row["bday"])
            if cur_bday.day == todays_date.day and cur_bday.month == todays_date.month:
                chan_file = open(str(guild.id) + "channel.txt", mode="r")
                channel = bot.get_channel(int(chan_file.read()))
                await channel.send(f":partying_face: :birthday:  Happy Birthday <@{row['user']}>!  :birthday: :partying_face:")