import os
import discord
from discord.ext import tasks
# you must make your own config.py file with GUILD, Channel, logdir, and token variables
import config

# Changing the CWD 
os.chdir(config.logdir)

messagelocation = []
save = []
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        if guild.name == config.GUILD:
            for channels in guild.channels:
                if (channels.name == config.Channel):
                    print(channels.id)
                    messagelocation.append(channels.id)
    await log_read.start()

@tasks.loop(seconds=10)
async def log_read():
    # retrieves logs from server
    logs = open("latest.log", "r")
    text = logs.read()
    log = text.split("\n")
    logs.close()

    # splits and cleans the text from logs
    for i in log:
        if i != "":
            log_split = i.split("]")
            save.append(log_split)

    # opens and reads the last logs printed
    logs = open("last.txt", "r")
    text = logs.read()
    log = text.split("\n")
    logs.close()

    # picks relevant logs cleans and prints them
    out = ""
    for i in save:
        if len(i) > 1:
            if i[2] == ' [net.minecraft.server.MinecraftServer/':
                if i[0] not in log:
                    await client.get_channel(messagelocation[0]).send(i[3].strip(":"))
        out = out + i[0] + "\n"

    #opens and writes to last file to track what has been sent
    logs = open("last.txt", "w")
    logs.write(out)
    logs.close

client.run(config.token)