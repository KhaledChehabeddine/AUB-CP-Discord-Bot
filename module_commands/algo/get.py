import json, inspect, discord
from helper.cEmbed import denied_msg
from helper.cLog import elog
from helper.Algorithm import Algorithm
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

    if args[0] in db_algo.keys(): algo = Algorithm(_id= args[0])
    else:
        if args[0] not in db_algo.inv.keys():
            await msg.reply(embed = denied_msg("Error", "Algorithm is not available."))
            return False
        else: algo = Algorithm(algo= args[0])

    if len(args) == 1: algo.lang = "cpp"
    else: algo.lang = args[1]

    if not algo.is_found():
        await msg.reply(embed = denied_msg("Error", "Algorithm is not available yet."))
        return False

    return algo

async def execute(msg, args, client):
    try:
        algo = await check_args(msg, args)
        if algo == False : return

        # check the case where the file is a zip file

        code = github_api.get_file(str(algo))
        file_path = config['module_cmds_loc'] + "/algo/code.txt"

        fs = open(file_path, "w")
        fs.write(code) 
        fs.close()

        await msg.channel.send(file= discord.File(file_path, str(algo)))

        fs = open(file_path, "w")
        fs.write("") 
        fs.close()
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())
    
