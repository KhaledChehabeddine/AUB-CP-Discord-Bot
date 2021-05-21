import json, inspect
from helper.User import User
from helper.cEmbed import granted_msg, denied_msg
from helper.GitHub import GitHub
from helper.cLog import elog
from cDatabase.DB_Algorithm import DB_Algorithm

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

github_api = GitHub()
db_algo = DB_Algorithm('db_algorithms')

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return True

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return  file + " [algorithm] [language] [code]"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Creates a new file in the repository."

# ------------------ [ check_args() ] ------------------ #
    # Checks if the command called by the user is valid
async def check_args(msg, args):
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        description = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", description))
        return False


    if ((len(msg.attachments) == 0 and (len(args) < 4 or len(args[0].split()) != 4))
        or (len(msg.attachments) == 1 and (len(args) != 1 or len(args[0].split()) != 4))):
        await msg.reply(embed = denied_msg("Invalid Command Format", usage()))
        return False

    if len(msg.attachments) != 0: 
        file_path = config['module_cmds_loc'] + "/algo/code.txt"
        await msg.attachments[0].save(file_path)
        
        fs = open(file_path, "r")
        code = fs.read()
        fs.close()
        fs = open(file_path, "w")
        fs.write("") 
        fs.close()

        language = msg.attachments[0].filename.split(".")[-1]
        args = args[0].split()[2:] + [language, code]
    else: 
        args = args[0].split()[2:] + [args[1].strip('`')] + ['\n'.join(args[2 : -1])]

    algorithm, language, code_language, code = args[0], args[1], args[2], args[3]

    if language not in ['cpp', 'java', 'py']:
        await msg.reply(embed = denied_msg("Invalid Language", "Try one of `cpp`, `java`, `py`"))
        return False

    if language != code_language:
        await msg.reply(embed = denied_msg("Invalid Code Spinnet", ""))
        return False

    if db_algo.find_algo(algorithm, language):
        await msg.reply(embed = denied_msg("Error", "Algorithm already exists in this language"))
        return False

    return args

async def execute(msg, args, client):
    try:
        args = await check_args(msg, args)
        if args == False: return

        db_algo.add_algo(args[0], args[1])

        filename = args[0] + '.' + args[1]
        code = args[3]

        result = github_api.add_file(filename, code)

        if result == True:
            await msg.channel.send(embed = granted_msg("Algorithm Added Succesfully", filename))
        else:
            elog(result, inspect.stack()) 
            await msg.reply(embed = denied_msg())
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())
    
