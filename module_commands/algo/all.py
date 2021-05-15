import json, inspect, discord
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog
from cDatabase.DB_Algorithm import DB_Algorithm

config = json.load(open('config.json', 'r'))

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

db_algo = DB_Algorithm('db_algorithms')

# ------------------ [ is_admin_only() ] ------------------ #
    # Limits this command to only admin users (i.e. Ahmad, Khaled, MB, Miguel)
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return  file

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Displays All Currently Available Algorithms"

async def execute(msg, args, client):
    try:
        algorithms, languages = str(), str()

        for (algo, lang_lst) in db_algo.items():
            algorithms += algo + "\n"
            languages += str(lang_lst) + "\n"

        if len(algorithms) == 0:
            await msg.reply(embed = denied_msg("No Available Algorithms Yet", ""))
            return

        response = granted_msg("Available Algorithms")

        response.add_field(
            name = "Algorithm",
            value = algorithms,
            inline = True
        )
        response.add_field(
            name = "Languages",
            value = languages,
            inline = True
        )

        await msg.channel.send(embed = response)
    
    except Exception as ex:
        elog(ex, inspect.stack()) 
        await msg.reply(embed = denied_msg())
    
