import json, inspect, discord
from helper.cEmbed import denied_msg, granted_msg
from helper.cLog import elog
from helper.User import User
from cDatabase.DB_Algorithm import DB_Algorithm
from helper.GitHub import GitHub

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

db_algo = DB_Algorithm('db_algorithms')
github_api = GitHub()

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return  file + " [algorithm] [language] [confimartion_key]"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Deletes the specified algorithm."

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        description = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", description))
        return False

    if len(args) != 3:
        await msg.reply(embed = denied_msg("Invalid Command Format", usage()))
        return False

    algorithm, language, key = args[0], args[1], args[2]

    if key != config['confirmation_key']:
        await msg.reply(embed = denied_msg("Invalid Confirmation Key", ""))
        return False

    if not db_algo.find_algo(algorithm, language):
        await msg.reply(embed = denied_msg("Error", "Algorithm is not available yet."))
        return False

    return [algorithm, language]

async def execute(msg, args, client):
    try:
        args = await check_args(msg, args)
        if args == False : return

        github_api.delete_file(args[0] + "." + args[1])
        db_algo.del_algo(args[0], args[1])

        await msg.channel.send(embed = granted_msg("Algorithm Deleted Successfully", ""))
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())
    
