import inspect, json
from helper.cLog import elog
from helper.cEmbed import granted_msg, denied_msg

config = json.load(open('config.json', 'r'))
prefix = config['prefix']
path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

# ------------------ [ is_admin_only() ] ------------------ #
    # Anybody can use this command
def is_admin_only(): return False

# ------------------ [ usage() ] ------------------ #
    # Returns how the command is called ex. "[prefix][command]"
def usage(): return prefix + file

# ------------------ [ description() ] ------------------ #
    # Returns a short explanation of what the function does
def description(): return "Displays info about this server."

# ------------------ [ execute() ] ------------------ #
    # Checks if server exists, throws an exception and sends "denied_msg" if an error occurs
    # Creates and sends an embed "response" with information of "message's" server 
    # Throws exception "ex" if any error occurs, logs it with "elog" and sends "denied_msg"
async def execute(msg, args, client):
    try:
        try:
            response = granted_msg(str(msg.guild.name) + " Info")
        except Exception:
            await msg.reply(embed = denied_msg("This is not a Server", ""))
            return
        response.set_thumbnail(url = msg.guild.icon_url)
        response.add_field(
            name = "Owner", 
            value = "<@!" + str(msg.guild.owner_id) + ">", 
            inline = False
        )
        response.add_field(
            name = "Region", 
            value = str(msg.guild.region), 
            inline = False
        )
        response.add_field(
            name = "Member Count", 
            value = str(msg.guild.member_count), 
            inline = False
        )
        await msg.channel.send(embed = response)
    except Exception as ex:
        elog(ex, inspect.stack())
        await msg.reply(embed = denied_msg())