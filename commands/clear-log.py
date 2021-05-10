import inspect, json
from helper.cLog import elog
from helper.cEmbed import denied_msg, granted_msg
from helper.User import User

config = json.load(open('config.json', 'r'))
prefix = config['prefix']

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

def is_admin_only(): return True

def usage():
  return prefix + file

def description():
  return "Clears the Error Log."

async def execute(msg, args, client):
  try:
    author = User(id = str(msg.author.id))
    if not author.is_admin():
        desc = msg.author.mention + " You are not allowed to use this function."
        await msg.reply(embed = denied_msg("Admin Command", desc))
        return None

    fs = open('./logs/error_log.txt', 'w')
    fs.seek(0)
    fs.truncate()
    fs.close()
    await msg.channel.send(embed = granted_msg("Error Log Cleared Successfully", ""))
  except Exception as ex:
    elog(ex, inspect.stack())
    await msg.reply(embed = denied_msg())