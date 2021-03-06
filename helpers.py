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
    bdays_file.close()
    bdays_file = open(str(ctx.guild.id) + "birthdays.txt", mode="w")
    csv_writer = csv.DictWriter(bdays_file, ["user", "bday"])
    for item in temp_bdays_dict.items():
        csv_writer.writerow({"user": item[0], "bday": item[1]})
    bdays_file.close()
    await ctx.send(f"Birthday for {ctx.author.display_name} updated successfully!")

async def change_channel(ctx, new_chan):
    new_chan_obj = discord.utils.get(ctx.guild.text_channels, name=new_chan)
    if new_chan_obj == None:
        await ctx.channel.send("That channel does not appear to exist, please try again.")
        return
    chan_file = open(str(ctx.guild.id) + "channel.txt", mode="w")
    chan_file.write(str(new_chan_obj.id))
    chan_file.close()
    await ctx.channel.send(f"Output channel successfully changed to {new_chan_obj.name}.")

async def list_bdays(ctx):
    bdays_file = open(str(ctx.guild.id) + "birthdays.txt", mode="r")
    csv_reader = csv.DictReader(bdays_file, ["user", "bday"])
    output = ""
    for row in csv_reader:
        if row["user"] == "user":
            continue
        user = discord.utils.get(ctx.guild.members, id=int(row["user"]))
        cur_bday = datetime.date.fromisoformat(row["bday"])
        if 4 <= cur_bday.day <= 20 or 24 <= cur_bday.day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][cur_bday.day % 10 - 1]
        if cur_bday.strftime("%d")[0] == "0":
            day = cur_bday.strftime("%d")[1]
        else:
            day = cur_bday.strftime("%d")
        cur_bday_str = cur_bday.strftime(f"{day}{suffix} of %B")
        output += user.display_name + "'s birthday is on the " + cur_bday_str + "." + "\n"
    chan_file = open(str(ctx.guild.id) + "channel.txt", mode="r")
    channel = ctx.guild.get_channel(int(chan_file.read()))
    await channel.send(output + "\nBirthdays listed above.")

async def check_bdays(bot):
    for guild in bot.guilds:
        bdays_file = open(str(guild.id) + "birthdays.txt", mode="r")
        csv_reader = csv.DictReader(bdays_file, ["user", "bday"])
        todays_date = datetime.date.today()
        for row in csv_reader:
            if row["user"] == "user":
                continue
            cur_bday = datetime.date.fromisoformat(row["bday"])
            if cur_bday.day == todays_date.day and cur_bday.month == todays_date.month:
                print("Birthday found!")
                chan_file = open(str(guild.id) + "channel.txt", mode="r")
                channel = bot.get_channel(int(chan_file.read()))
                await channel.send(f":partying_face: :birthday:  Happy Birthday <@{row['user']}>!  :birthday: :partying_face:")