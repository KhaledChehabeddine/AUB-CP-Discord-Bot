import inspect, json
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog

config = json.load(open('config.json', 'r'))
prefix = config['prefix']

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

def is_admin_only(): return False

def description():
  return ("Displays info about this server.\n"
          + "**Usage:** `" + prefix + file + "`")

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