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

webhook_url="https://discordapp.com/api/webhooks/856696688437755934/9NW-2w46XZp-Sd2TmZuJTAg2hz7FVFPVDt4VY_7ZnXf_5yhjB1yQHGFe_Eh23KXMj8aM"

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
    main_url = f"https://api.playswagiq.com/trivia/home?_uid="
    headers = {
               "Authorization": f"Bearer {BEARER_TOKEN}",
               "user-agent": "SwagIQ-Android/34 (okhttp/3.10.0)"
              }
    try:
        response_data = requests.post(url=main_url, headers=headers).json()
        print(response_data)
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)

    if "joinable" not in response_data or response_data["joinable"] is None or response_data["joinable"] != "True":
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            print("Show not on.")
            hook.send("Show not on.")



def show_active():
    main_url = 'https://api.playswagiq.com/trivia/home?_uid='
    headers = {"Authorization": "Bearer BoevwXaFzGYgR3WKHrH8L_tmGb0j_3k6a-dMEN2Z4iQPZiTHQ0uO9QKaR4NMf7H95hNUvf0LMO3aKVi031S7gVoc4yP_2w",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    return response_data['episode']['startDisplay']


def get_socket_url():
    main_url = 'https://api.playswagiq.com/trivia/join?_uid='
    headers = {"Authorization": "Bearer BoevwXaFzGYgR3WKHrH8L_tmGb0j_3k6a-dMEN2Z4iQPZiTHQ0uO9QKaR4NMf7H95hNUvf0LMO3aKVi031S7gVoc4yP_2w",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    if response_data["success"] != "False":
        id = response_data["viewId"]
        socket_url = f"wss://api.playswagiq.com/sock/1/game/{id}?_uid="
    
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)
            if 'comments' not in message_data:
                try:
                    hook.send(message_data)
                except:
                    print(message_data)
            if "question" in message_data:
                try:
                    hook.send(message_data["question"])
                except:
                    print(message_data["question"])
            elif "answerResults" in message_data:
                try:
                    hook.send(message_data["answerResults"])
                except:
                    print(message_data["answerResults"])
            
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
