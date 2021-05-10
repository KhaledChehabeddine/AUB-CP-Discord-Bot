import os, inspect, discord, json, importlib , asyncio
from helper.cLog import elog
from helper.cEmbed import denied_msg, contest_msg
from helper.User import User
from cDatabase.DB_Users import DB_Users
from helper.CF_API import CF_API

config = json.load(open('config.json', 'r'))
prefix = config['prefix']

av_cmds = dict()
db_users = DB_Users('db_users')
cf_api = CF_API()

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

async def my_background_task():
  await client.wait_until_ready()
  await asyncio.sleep(2)
 
  while not client.is_closed():
    for (k, v) in db_users.items():
      await asyncio.sleep(5)
      user = User(id = k, handle = v, client = client)
      rank = cf_api.user_rank(user)
      if await user.has_role(rank): continue
      lst = await user.get_lower_roles(rank)
      for r in lst:
        await user.remove_role(r)
      await user.add_role(rank)
    
    await asyncio.sleep(3 * 60 * 60)

client.loop.create_task(my_background_task())
client.run(config['token'])