import os
import discord
my_discord_TOKEN = os.environ['TOKEN']
my_codeforces_key = os.environ['CF_KEY']
my_codeforces_secret = os.environ['CF_SECRET']


import requests
import json

import datetime


client = discord.Client()

def get_quote():
  response = requests.get("http://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' ' + " - " + json_data[0]['a']
  return quote
  # return json_data
  
def get_upcoming_contests():
  response = requests.get("https://codeforces.com/api/contest.list")
  contests_data = json.loads(response.text)

  contest_details = "";

  for i in range(20,-1,-1):
    contest_name = contests_data['result'][i]['name']
    contest_phase = contests_data['result'][i]['phase']
    contest_duration = int(contests_data['result'][i]['durationSeconds'])
    contest_startTimeSeconds = contests_data['result'][i]['startTimeSeconds']
    contest_startTimeSeconds+=19800

    contest_hrs = (contest_duration/60)/60;
    contest_mins = (contest_duration/60)%60;

    contest_dateandtime = datetime.datetime.fromtimestamp(contest_startTimeSeconds).strftime('%c')

    print(contest_dateandtime)
    


    if(contest_phase == "BEFORE"):
      contest_details = contest_details  + contest_name + '         ' + contest_dateandtime  + '       ' + str(int(contest_hrs)) +'hrs ' + str(int(contest_mins)) + 'mins ' + '\n\n'
  
  return contest_details

# print(get_quote())
# print(get_upcoming_contests())

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event 
async def on_message(message):
  if( message.author == client.user):
    return

  if message.content.startswith('cf;hello'):
    await message.channel.send('Hello');

  if message.content.startswith('cf;inspire'):
    quote = get_quote()
    await message.channel.send(quote);

  if message.content.startswith('cf;upcoming'):
    contests = get_upcoming_contests()
    await message.channel.send(contests);

client.run(my_discord_TOKEN) 
