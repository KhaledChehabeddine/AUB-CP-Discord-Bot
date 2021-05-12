import os, importlib, json, inspect
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog

config = json.load(open('config.json', 'r'))
prefix = config['prefix']
path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]
available_commands = dict()
available_modules = dict()

# ------------------ [ is_admin_only() ] ------------------ #
    # Anybody can use this command
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return prefix + file

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Displays the information about commands provided by the bot."

# ------------------ [ init() ] ------------------ #
    # Iterates over names in "folder" file of "config["cmds_loc"]"
    # Verifies if name is a command by checking if last 3 letters == ".py"
    # Commands added to "available_commands", otherwise skipped
def init():
    try:
        for (t1, t2, folder) in os.walk(config['cmds_loc']):
            for item in folder:
                if item[-3:] != '.py': continue
                available_commands[item[:-3]] = importlib.import_module(config['cmds_loc'][2:] + '.' + item[:-3])

        for (path, general_folder, folder) in os.walk(config['module_cmds_loc']):
            for inner_folder in general_folder: available_modules[inner_folder] = {}
            current_folder = path.split(config["split_path"])[-1]
            for item in folder:
                if item[-3:] != ".py": continue
                file_path = config['module_cmds_loc'][2:] + "." + current_folder + "." + item[:-3]
                available_modules[current_folder][item[:-3]] = importlib.import_module(file_path)
    except Exception as ex: elog(ex, inspect.stack())

# ------------------ [ execute() ] ------------------ #
    # Checks if there are commands in "available_commands"
    # Adds only non-admin commands into the embed
    # Throws an exception if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        if len(available_commands) == 0: init()

        response = granted_msg("Bot Modules")
        for module in available_modules:
            module_msg = ""
            for cmd in available_modules[module].keys():
                if available_modules[module][cmd].is_admin_only(): continue
                module_msg += cmd + "\n"
            if len(module_msg) == 0: continue
            response.add_field(
                name = module, 
                value = "```\n" + module_msg + "\n```", 
                inline = True
            )
        await msg.channel.send(embed = response)

        response = granted_msg("Bot Commands")
        for cmd in available_commands:
            if available_commands[cmd].is_admin_only(): continue
            response.add_field(
                name = available_commands[cmd].usage(), 
                value = available_commands[cmd].description(), 
                inline = False
            )
        await msg.channel.send(embed = response)
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())