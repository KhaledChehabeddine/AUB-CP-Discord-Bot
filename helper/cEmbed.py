import discord, json
from helper.cTime import MyDate

config = json.load(open('config.json', 'r'))
icon_url = config['icon_url']

def granted_msg(_title, desc = ""):
  response = discord.Embed(
    title = _title,
    description = desc,
    color = discord.Color.green(),
  )
  response.set_footer(
    text = "CodeX • " + MyDate().footer(),
    icon_url = icon_url
  )
  return response

def denied_msg(
 _title = "Error Message", 
 desc = ("There was an error while executing the command.\n"
  + "The error has been logged and will be fixed shortly.")
):
  response = discord.Embed(
    title = _title,
    color = discord.Color.red(),
  )
  response.description = desc
  response.set_footer(
    text = "CodeX • " + MyDate().footer(),
    icon_url = icon_url
  )
  return response

def contest_msg(k, v, dt):
  response = discord.Embed(
    title = v['name'],
    color = discord.Color.blue(),
    description = "[**REGISTER**](https://codeforces.com/contestRegistration/" + k + ")"
  )

  if (dt == 1440): left = "24 Hours"
  if (dt == 360): left = "6 Hours"
  if (dt == 15): left = "15 Minutes" 
  
  response.add_field(name = "Date", value = v['date'], inline = False)
  response.add_field(name = "Duration", value = v['duration'], inline = True)
  response.add_field(name = "Time Left", value = left, inline = True)

  response.set_footer(
    text = "xCode • " + MyDate().footer(),
    icon_url = icon_url
  )

  return response