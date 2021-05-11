# ------------------ [ Authors: ] ------------------ #
    # Ahmad Zaaroura
    # Khaled Chehabeddine
    # Miguel Merheb

import os
import inspect
import discord
import json
import importlib
import asyncio
from helper.cLog import elog
from helper.cEmbed import denied_msg
from helper.User import User
from cDatabase.DB_Users import DB_Users
from helper.CF_API import CF_API


config = json.load(open('config.json', 'r'))
prefix = config['prefix']
client = discord.Client()
available_commands = dict()
db_users = DB_Users('db_users')
cf_api = CF_API()

# ------------------ [ init() ] ------------------ #
    # Iterates over names in "folder" file of "config["cmds_loc"]"
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
    # Sets bot status to "playing [prefix]help"
@client.event
async def on_ready(): 
    init()
    await client.change_presence(activity = discord.Game(prefix + "help"))
    #await client.change_presence(status = discord.Status.offline)
    print("KFC Bot online.")

# ------------------ [ on_message() ] ------------------ #
    # Runs after a user sends a message
    # Checks if command called is not empty ex. "[prefix]"
    # Checks if command called is in "available_commands"
    # Throws an exception if any occurs while running, logged using "elog()" function
        # Error message "denied_msg" sent to appropriate channel
@client.event
async def on_message(message):
    try:
        if message.content[:len(prefix)] != prefix or message.author.bot: return
        arguments = message.content[len(prefix):].split()

        if (len(arguments) == 0): return
        command = arguments[0]

        if not command in available_commands.keys(): return
        await available_commands[command].execute(message, arguments[1:], client)

    except Exception as ex:
        elog(ex, inspect.stack()) 
        await message.reply(embed = denied_msg())

async def my_background_task():
  await client.wait_until_ready()
  await asyncio.sleep(2)
 
  while not client.is_closed():
    for (k, v) in db_users.items():
      await asyncio.sleep(5)
      user = User(id = k, handle = v, client = client)
      rank = cf_api.user_rank(user)
      if await user.has_role(rank): continue
      lst = await user.get_different_roles(rank)
      for r in lst:
        await user.remove_role(r)
      await user.add_role(rank)
    
    await asyncio.sleep(3 * 60 * 60)

client.loop.create_task(my_background_task())
client.run(config['token'])