import inspect, json
from helper.cLog import elog
from helper.cEmbed import granted_msg, denied_msg

config = json.load(open('config.json', 'r'))
prefix = config['prefix']

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

def is_admin_only(): return False

def usage():
  return prefix + file

def description():
  return "Shows User's Dircord Identification Card."

async def execute(msg, args, client):
  try:
    user = msg.author

    response = granted_msg(
      "Discord Identification Card", 
      "This is a description of user: " + str(user)
    )

    response.set_thumbnail(url = user.avatar_url)
    response.add_field(
      name = "Name: ", 
      value = user.name, 
    )
    response.add_field(
      name = "ID: ", 
      value = user.id,
    )
    response.add_field(
      name = '\u200b',
      value = '\u200b'
    )
    try:
      response.add_field(
        name = "Nickname: ", 
        value = user.nick, 
      )
      response.add_field(
        name = "Top Role: ", 
        value = user.top_role.name, 
      )
    except Exception: pass
    
    await msg.channel.send(embed = response)
  except Exception as ex:
    elog(ex, inspect.stack())
    await msg.reply(embed = denied_msg())