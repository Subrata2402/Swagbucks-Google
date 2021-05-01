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
import aiohttp
import asyncio
ids1 = []
ids2 = []
ids3 = []

webhook_url="webhook url"

try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")
                    
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
        print(response_data)
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)

    if "broadcast" not in response_data or response_data["broadcast"] is None:
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            print("Show not on.")
            tim = (response_data["nextShowTime"])
            tm = aniso8601.parse_datetime(tim)
            x =  tm.strftime("%H:%M")
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            x_in = x_ind.strftime("%d/%m/%Y")
            x_inn = x_ind.strftime("%H:%M")
    
            prize = (response_data["nextShowPrize"])
            time.sleep(5)
            print(x_in)
            print(prize)



def show_active():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    return response_data['active']


def get_socket_url():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()

    socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "x-hq-client": "iPhone8,2"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)
            if message_data['type'] != 'interaction':
                print(message_data)
        
            if message_data['type'] == 'question':
                question = message_data['question']
                qcnt = message_data['questionNumber']
                Fullcnt = message_data['questionCount']
                id1 = message_data["answers"][0]["answerId"]
                ids1.append(id1)
                id2 = message_data["answers"][1]["answerId"]
                ids2.append(id2)
                id3 = message_data["answers"][2]["answerId"]
                ids3.append(id3)

            elif message_data['type'] == 'answered':
                user = ""
                answ = ""
                name = message_data["username"]
                ans = message_data["answerId"]
                if name == 'Xhide':
                    user = "Mohit Raj"
                elif name == 'angelalai':
                    user = "Only Fun"
                elif name == 'TheBigHQ':
                    user = "Ethann 1"
                elif name == 'ThatHQGuy':
                    user = "Ethann 2"
                elif name == 'maatya2':
                    user = "Cool Yash"
                op1 = list(ids1)
                op2 = list(ids2)
                op3 = list(ids3)
                for a in op1:
                    print(a)
                for b in op2:
                    print(b)
                for c in op3:
                    print(c)
                if a == ans:
                    answ = "Option 1"
                if b == ans:
                    answ = "Option 2"
                if c == ans:
                    answ = "Option 3"
                embed = discord.Embed(title=f"``{user}`` : **{answ}**",description="",color=0x00ff00)
                hook.send(embed=embed)

            elif message_data["type"] == "questionClosed":
                embed=discord.Embed(title=":alarm_clock: Time,s UP",description="",color=0xa1fc03)
                time.sleep(5)
                ids1.clear()
                ids2.clear()
                ids3.clear()

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
        token = get_auth_token()
        if token == 'NONE':
            print('Please enter a valid auth token.')
        else:
            connect_websocket(url, token)
    else:
        show_not_on()
        time.sleep(300)
