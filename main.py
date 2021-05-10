import os, inspect, discord, json, importlib 
from helper.cLog import elog
from helper.cEmbed import denied_msg, contest_msg

config = json.load(open('config.json', 'r'))
prefix = config['prefix']

av_cmds = dict()

def init():
  try:
    for (r, d, f) in os.walk(config['cmds_loc']):
      for item in f:
        if item[-3:] != '.py': continue
        av_cmds[item[:-3]] = importlib.import_module(config['cmds_loc'][2:] + '.' + item[:-3])
  except Exception as ex:
    elog(ex, inspect.stack())

############################################################################
############################################################################
############################################################################

client = discord.Client()

@client.event
async def on_ready(): 
    init()
    await client.change_presence(activity = discord.Game(prefix + "help"))
    #await client.change_presence(status = discord.Status.offline)
    print("Bot Online")
  
@client.event
async def on_message(msg):
  try:
    if msg.content[:len(prefix)] != prefix or msg.author.bot: return

    args = msg.content[len(prefix):].split()
    if (len(args) == 0): return
    cmd = args[0]

    if not cmd in av_cmds.keys(): return

    await av_cmds[cmd].execute(msg, args[1:], client)

  except Exception as ex:
    elog(ex, inspect.stack()) 
    await msg.reply(embed = denied_msg())

client.run(config['token'])
