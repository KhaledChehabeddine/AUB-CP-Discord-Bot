import inspect, json
from helper.cLog import elog
from helper.cEmbed import denied_msg
from helper.User import User

config = json.load(open('config.json', 'r'))
prefix = config['prefix']

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

def is_admin_only(): return True

def usage():
  return prefix + file

def description():
  return "Displays the Error Log."

async def execute(msg, args, client):
  try:
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        desc = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", desc))
        return None

    fs = open('./logs/error_log.txt', 'r')
    s = ""
    for line in  fs.readlines(): s += line + '\n'
    
    if (len(s) == 0):
      await msg.reply(embed = denied_msg("Error Log is Empty", ""))
      return

    await msg.channel.send("```" + s + "```")
    fs.close()
  except Exception as ex:
    elog(ex, inspect.stack())
    await msg.reply(embed = denied_msg())