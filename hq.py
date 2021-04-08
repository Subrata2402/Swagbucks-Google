import discord
import webbrowser
from termcolor import colored
import datetime
import logging
import os
#import Google_Search
import time
from datetime import datetime
from pytz import timezone
from lomond import WebSocket
from unidecode import unidecode
import colorama
import requests
import json
import re
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed
import aniso8601
from time import sleep


webhook_url="https://discordapp.com/api/webhooks/826977215220678686/sgLdymliajzTbg4KbecpOtyG2DZZbs1dIWxcx1xbs2PHjdIB2hHs8j6R6UdIJQN--8S4"

we="https://discordapp.com/api/webhooks/826977215220678686/sgLdymliajzTbg4KbecpOtyG2DZZbs1dIWxcx1xbs2PHjdIB2hHs8j6R6UdIJQN--8S4"


try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")


try:
    hq = Webhook(we)
except:
    print("Invalid WebHook Url Lol")

main_url = 'https://api-quiz.hype.space/shows/now'
response_data = requests.get(main_url).json()
tim = (response_data["nextShowTime"])
tm = aniso8601.parse_datetime(tim)
x_ind = tm.astimezone(timezone("Asia/Kolkata"))
time = x_ind.strftime("%d-%m-%Y %I:%M %p")
prize = (response_data["nextShowPrize"])
for data in response_data["upcoming"]:
    type = data["nextShowLabel"]["title"]
embed=discord.Embed(title="**__HQ Next Show Details !__**", description=f"**• Show Name : {type}\n• Show Time : {time}\n• Prize Money : {prize}**", color=0x00FBFF)
embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/799237115962851348/816261537101905951/1200px-HQ_logo.svg.png")
hook.send(embed=embed)

def show_not_on():
    colorama.init()
    # Set up logging
    logging.basicConfig(filename="data.log", level=logging.INFO, filemode="w")

    # Read in bearer token and user ID
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            BEARER_TOKEN = settings[0].split("=")[1]
        except IndexError as e:
            logging.fatal(f"Settings read error: {settings}")
            raise e

    print("getting")
    main_url = f"https://api-quiz.hype.space/shows/now?type="
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "x-hq-client": "Android/1.3.0"}
    # "x-hq-stk": "MQ==",
    # "Connection": "Keep-Alive",
    # "User-Agent": "okhttp/3.8.0"}

    try:
        response_data = requests.get(main_url).json()
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)

    if "broadcast" not in response_data or response_data["broadcast"] is None:
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            print("Show not on.")
            

def show_active():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    #print(response_data)
    return response_data['active']
    


def get_socket_url():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    socket_url = response_data['broadcast']['socketUrl']
    #if socket_url != None:
        #return print("Show is live.")
    socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "x-hq-client": "iPhone8,2"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        #print(msg)
        if msg.name == "text":
            message = msg.text
            #print(message)
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            print(message)
            message_data = json.loads(message)
            #print(message_data)

            if message_data['type'] == 'startRound':
                hint = message_data["hint"]
                puzzleState = message_data["puzzleState"]
                round_number = message_data["roundNumber"]
                total_round = message_data["totalRounds"]
                embed=discord.Embed(title=f"**Round {round_number} out of {total_round}**", color=0x00ffff)
                embed.add_field(name="**Hint :-**", value=f"**{hint}**")
                embed.add_field(name="**Puzzle :-**", value=f"{puzzleState}")
                #description=f"**● Correct Answer: {answer}\n● Hint: {hint}\n● Advancing Players: {advancing}\n● Eliminated Players: {eliminated}\n● Found Letters: {letter}**", color=0x00ffff)
                embed.set_footer(text="HQ Words | Subrata#3297")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/814483066013351949/829424156348383283/IMG_20210329_102247.jpg")
                hook.send(embed=embed)

            elif message_data["type"] == "endRound":
                answer = message_data["answer"]
                round_number = message_data["roundNumber"]
                total_round = message_data["totalRounds"]
                advancing = message_data["correctAnswers"]
                eliminated = message_data["incorrectAnswers"]
                embed=discord.Embed(title=f"**Round {round_number} out of {total_round}**", color=0x00ff00)
                embed.add_field(name="**Correct Answer :-**", value=f"**{answer}**")
                embed.add_field(name="**Status :-**", value=f"**• Advancing Players: {advancing}\n• Eliminated Players: {eliminated}**")
                #description=f"**● Correct Answer: {answer}\n● Hint: {hint}\n● Advancing Players: {advancing}\n● Eliminated Players: {eliminated}\n● Found Letters: {letter}**", color=0x00ffff)
                embed.set_footer(text="HQ Words | Subrata#3297")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/814483066013351949/829424156348383283/IMG_20210329_102247.jpg")
                hook.send(embed=embed)

            elif message_data["type"] == "gameSummary":
                winn = message_data['numWinners']
                prizeMoney = str(message_data["winners"][0]["prize"])
                embed=discord.Embed(title="**__Game Summary !__**",description=f"**● Payout: {prizeMoney}\n● Total Winners: {winn}\n● Prize Money: $5,000**",color=0x00FBFF)
                #embed.add_field(name="**__First Three Winners !__**", value=f"**● {name1} – {prize1}\n● {name2} – {prize2}\n● {name3} – {prize3}**")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737764195743039488/737768505935659178/giphy1.gif")
                embed.set_footer(text=f"HQ Google | Subrata#3297", icon_url="")
                hook.send(embed=embed)
                #hq.send(embed=embed)




"""
def open_browser(question):

    main_url = "https://www.google.co.in/search?q=" + question
    webbrowser.open_new(main_url)
"""

def get_auth_token():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            auth_token = settings[0].split("=")[1]
        except IndexError:
            print('No Key is given!')
            return 'NONE'

        return auth_token

while True:
    if show_active():
        url = get_socket_url()
        #print('Connecting to Socket : {}'.format(url))
        #hook.send('Connecting to Socket : {}'.format(url))

        token = get_auth_token()
        if token == 'None':
            print('Please enter a valid auth token.')
        else:
            connect_websocket(url, token)

    else:
        show_not_on()
        time.sleep(300)
