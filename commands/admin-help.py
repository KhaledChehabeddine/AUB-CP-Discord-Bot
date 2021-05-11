import os, importlib, json, inspect
from helper.cLog import elog
from helper.cEmbed import granted_msg, denied_msg
from helper.User import User

config = json.load(open('config.json', 'r'))
prefix = config['prefix']
path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]
available_commands = dict()

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return prefix + file

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Displays the information about admin commands provided by the bot."

# ------------------ [ init() ] ------------------ #
    # Iterates over names in "folder" file of "config["cmds_loc"]"
    # Verifies if name is a command by checking if last 3 letters == ".py"
    # Commands added to "available_commands", otherwise skipped
def init():
    for (t1, t2, folder) in os.walk(config['cmds_loc']):
        for item in folder:
            if item[-3:] != '.py': continue
            available_commands[item[:-3]] = importlib.import_module(config['cmds_loc'][2:] + '.' + item[:-3])

# ------------------ [ execute() ] ------------------ #
    # Checks if there are commands in "available_commands"
    # Checks if the author is an admin, returns "denied_msg" if true, otherwise "granted_msg"
    # Adds only admin commands into the embed
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        if len(available_commands) == 0: init()

        author = User(id = str(msg.author.id))
        if not author.is_admin():
            desc = msg.author.mention + " You are not allowed to use this function."
            await msg.reply(embed = denied_msg("Admin Command", desc))
            return

        response = granted_msg("Admin Commands")
        for cmd in available_commands:
            if not available_commands[cmd].is_admin_only(): continue
            response.add_field(
                name = prefix + cmd, 
                value = available_commands[cmd].description(), 
                inline = False
            )
        await msg.channel.send(embed = response)
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())