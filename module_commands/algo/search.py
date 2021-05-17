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
def usage(): return file + " [algorithm] + (language)"

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "searches Available Algorithms"

async def execute(msg, args, client):
    try:
        if len(args) == 0 or len(args[0]) == 0:
            await msg.reply(embed = denied_msg("Invalid Search Query", ""))
            return
        
        keyword = args[0]
        language = (args[1] if len(args) > 1 else None)
        algorithms, languages = str(), str()

        for (algo, lang_lst) in db_algo.items():
            if keyword not in algo: continue
            if language != None and language not in lang_lst: continue
            algorithms += algo + "\n"
            languages += str(lang_lst) + "\n"

        if len(algorithms) == 0:
            await msg.reply(embed = denied_msg("Empty Search Results", ""))
            return

        title = "Search Results for `algo= '" + keyword + "'`"
        if language != None: title += ", `lang= '" + language + "'`"
        response = granted_msg(title)

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