import os, importlib, json, inspect
from helper.cEmbed import granted_msg, denied_msg
from helper.cLog import elog

config = json.load(open('config.json', 'r'))
prefix = config['prefix']

path = __file__.split(config['split_path'])
file = path[len(path) - 1][:-3]

def is_admin_only(): return False

def description():
  return ("Displays the information about commands provided by the bot.\n"
        + "**Usage:** `" + prefix + file + "`")

av_cmds = dict()

def init():
  for (r, d, f) in os.walk(config['cmds_loc']):
    for item in f:
      if item[-3:] != '.py': continue
      av_cmds[item[:-3]] = importlib.import_module(config['cmds_loc'][2:] + '.' + item[:-3])

async def execute(msg, args, client):
  try:
    if len(av_cmds) == 0: init()      

    response = granted_msg("Bot Commands")
    for cmd in av_cmds:
      if av_cmds[cmd].is_admin_only(): continue
      response.add_field(
        name = prefix + cmd, 
        value = av_cmds[cmd].description(), 
        inline = False
      )
    await msg.channel.send(embed = response)

  except Exception as ex:
    elog(ex, inspect.stack())
    await msg.reply(embed = denied_msg())