# ------------------ [ Authors: ] ------------------ #
    # Ahmad Zaaroura
    # Khaled Chehabeddine
    # Miguel Merheb

import os
import json
import discord
import inspect
import importlib
from helper.cLog import elog
from helper.cEmbed import denied_msg, contest_msg

config = json.load(open('config.json', 'r'))
prefix = config['prefix']
client = discord.Client()
available_commands = dict()

# ------------------ [ init() ] ------------------ # 
    # Iterates over names in "folder" file
    # Verifies if name is a command by checking if last 3 letters == ".py"
    # Commands added to "available_commands", otherwise skipped
    # Throws an exception if any error occurs while running, logged using "elog()" function
def init():
    try:
        for (t1, t2, folder) in os.walk(config['cmds_loc']):
            for item in folder:
                if item[-3:] != '.py': continue
                available_commands[item[:-3]] = importlib.import_module(config['cmds_loc'][2:] + '.' + item[:-3])
    except Exception as ex: elog(ex, inspect.stack())

# ------------------ [ on_ready() ] ------------------ #
    # Runs after running main.py
    # Calls [ init() ]
    # Sets bot status to "playing >help"
@client.event
async def on_ready(): 
    init()
    await client.change_presence(activity = discord.Game(prefix + "help"))
    #await client.change_presence(status = discord.Status.offline)
    print("KFC Bot online.")

# ------------------ [ on_message() ] ------------------ #
    # Runs after a user sends a message
    # Checks if command called is not empty ex. ">"
    # Checks if command called is in "available_commands"
    # Throws an exception if any occurs while running, logged using "elog()" function
        # Error message "denied_msg" sent to appropriate channel
@client.event
async def on_message(msg):
    try:
        if msg.content[:len(prefix)] != prefix or msg.author.bot: return
        arguments = msg.content[len(prefix):].split()

        if (len(arguments) == 0): return
        command = arguments[0]

        if not command in available_commands.keys(): return
        await available_commands[command].execute(msg, args[1:], client)

    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())

client.run(config['token'])