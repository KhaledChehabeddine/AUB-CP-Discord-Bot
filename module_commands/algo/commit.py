import json, inspect
from helper.User import User
from helper.cEmbed import granted_msg, denied_msg
from helper.GitHub import GitHub
from helper.cLog import elog

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

github_api = GitHub()

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

    args = args[0].split()[2:] + [args[1].strip('`')] + ['\n'.join(args[2 : len(args) - 1])]

    if len(args) != 4:
        await msg.reply(embed = denied_msg("Invalid Command Format", usage()))
        return False

    algorithm, language, code_language, code = args[0], args[1], args[2], args[3]

    # check if language is valid
    # check if algorithm already exists

    if language != code_language:
        await msg.reply(embed = denied_msg("Invalid Code Spinnet", ""))
        return False

    return args

async def execute(msg, args, client):
    try:
        args = await check_args(msg, args)
        if args == False: return

        # add algo to database

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
    
