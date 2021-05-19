import json, inspect, discord
from helper.cEmbed import denied_msg
from helper.cLog import elog
from cDatabase.DB_Algorithm import DB_Algorithm
from helper.GitHub import GitHub

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

db_algo = DB_Algorithm('db_algorithms')
github_api = GitHub()

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return  file + " [algorithm] (language)"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Gets the code of the specified algorithm."

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    if len(args) < 1:
        await msg.reply(embed = denied_msg("Invalid Command Format", usage()))
        return False

    algorithm = args[0]

    if len(args) == 1: language = "cpp"
    else: language = args[1]

    if not db_algo.find_algo(algorithm, language):
        await msg.reply(embed = denied_msg("Error", "Algorithm is not available yet."))
        return False

    return [algorithm.lower(), language.lower()]

async def execute(msg, args, client):
    try:
        args = await check_args(msg, args)
        if args == False : return

        code = github_api.get_file(args[0] + "." + args[1])
        file_path = config['module_cmds_loc'] + "/algo/code.txt"

        fs = open(file_path, "w")
        fs.write(code) 
        fs.close()

        await msg.channel.send(file= discord.File(file_path, args[0] + "." + args[1]))

        fs = open(file_path, "w")
        fs.write("") 
        fs.close()
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())
    
