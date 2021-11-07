import discord
import webbrowser
from termcolor import colored
import datetime
import logging
import os
import time
from datetime import datetime, timedelta
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

BEARER_TOKEN = "BsfoofrVDTlZAVoF2Okav7luCBoy0QASbbRqhyMoOQ7N2CsvgXNdDXSh5yzbUQ5W4xxcuJGdqYKfOwszAIk1OZLxRmtcOw"

webhook_url="https://discord.com/api/webhooks/870090289514172487/qvev9wHUqOuR9k0q9hC8eFH4wMO-Ym8DjpXu1NHaKa-xzYAH4L1hMQ6l-1-AkGaecs-h"
web_url = "https://discord.com/api/webhooks/857113978534232064/h4a4RBLkl4AfLXnhehEq4OECRS3x9t_16nJO95XCbgN7irSsSE8ldEQKPDZ8NsDt0-8b"

try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")

try:
    sbl = Webhook(web_url)
except:
    print("Invalid WebHook Url!")

web_url = "https://discord.com/api/webhooks/874331448696520747/2So76G_t_0U-_Zz-08wLYOnSVFwcy-CM3e13sFVc3b8nEGJVH4jEkpgVLJvjSG3evpzv"

try:
    sbm = Webhook(web_url)
except:
    print("Invalid WebHook Url!")

def show_not_on():
    main_url = f"https://api.playswagiq.com/trivia/home?_uid="
    headers = {
               "Authorization": f"Bearer {BEARER_TOKEN}",
               "user-agent": "SwagIQ-Android/34 (okhttp/3.10.0)"
              }
    try:
        response_data1 = requests.post(url=main_url, headers=headers).json()
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    main_url = 'https://api.playswagiq.com/trivia/join?_uid='
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    if response_data["success"] == False:
        print("Show not on.")
        data = response_data1
        title = data["episode"]["title"]
        prize = data["episode"]["grandPrizeDollars"]
        pt = prize*100
        prize = '{:,}'.format(int(prize))
        time = data["episode"]["start"]
        r = datetime.fromtimestamp(time)
        time_change = timedelta(hours=5, minutes=30)
        new_time = r + time_change
        time = new_time.strftime("%d-%m-%Y %I:%M %p")
        embed=discord.Embed(title="**__SwagIQ Next Show Details !__**", description=f"**• Show Name : Swagbucks Live\n• Show Time : {time}\n• Prize Money : ${prize}**", color=discord.Colour.random())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/840841165544620062/843859541627764776/762971334774489111.png")
        embed.set_footer(text="Swagbucks Live")
        embed.timestamp = datetime.utcnow()
        sbl.send(embed=embed)
        #sbm.send(embed=embed)
        #hook.send(embed=embed)

def show_active():
    main_url = 'https://api.playswagiq.com/trivia/join?_uid='
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    return response_data['success']

def prize_money():
    main_url = f"https://api.playswagiq.com/trivia/home?_uid="
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "user-agent": "SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    prize = response_data["episode"]["grandPrizeDollars"]
    prize = '{:,}'.format(int(prize))
    return prize

def current_prize():
    main_url = f"https://api.playswagiq.com/trivia/home?_uid="
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "user-agent": "SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    prize = response_data["episode"]["grandPrizeDollars"]
    pay = prize*100
    return pay

def get_socket_url():
    main_url = 'https://api.playswagiq.com/trivia/join?_uid='
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"}
    response_data = requests.post(url=main_url, headers=headers).json()
    #if response_data["success"] != False:
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
            if message_data["code"] != 21:
                print(message_data)
            if message_data["code"] == 41:
                qn = message_data["question"]["number"]
                tqn = message_data["question"]["totalQuestions"]
                optid1 = message_data["question"]["answers"][0]["id"]
                optid2 = message_data["question"]["answers"][1]["id"]
                optid3 = message_data["question"]["answers"][2]["id"]
                try:
                    sb = message_data["question"]["sb"]
                except:
                    sb = 0
                embed=discord.Embed(title=f"**Question {qn} out of {tqn}**", description=f"**SB for this Question : 0{sb}**", color=discord.Colour.random())
                embed.add_field(name="**Options Id :-**", value=f"**１. {optid1}\n２. {optid2}\n３. {optid3}**")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/840841165544620062/843859541627764776/762971334774489111.png")
                embed.set_footer(text=f"Swagbucks Live")
                embed.timestamp = datetime.utcnow()
                sbm.send(embed=embed)
                hook.send(embed=embed)
                #sbm.send("-")
                #hook.send("s")
                time.sleep(10)
                embed=discord.Embed(title="**⏰ | Time's Up!**", color=discord.Colour.random())
                sbm.send(embed=embed)
                hook.send(embed=embed)
            if message_data["code"] == 42:
                ansid = message_data["correctAnswerId"]
                s = 0
                e = 0
                for answer in message_data["answerResults"]:
                    if answer["answerId"] == ansid:
                        advancing = answer["numAnswered"]
                        pA = answer["percent"]
                    else:
                        anNum = answer["numAnswered"] 
                        s = s + anNum
                        percent = answer["percent"]
                        e = e + percent
                pay = int(current_prize())/(int(advancing))
                payout = int(pay) + int(qn)
                if ansid == optid1:
                    option = f"Option １. {optid1}"
                if ansid == optid2:
                    option = f"Option ２. {optid2}"
                if ansid == optid3:
                    option = f"Option ３. {optid3}"
                embed=discord.Embed(title=f"**Question {qn} out of {tqn}**", color=discord.Colour.random())
                embed.add_field(name="**Correct Answer :-**", value=f"**{option}**")
                embed.add_field(name="**Status :-**", value=f"**• Advancing Players : {advancing} ({pA}%)\n• Elimineted Players : {s} ({e}%)\n• Current Payout : {payout}SB**")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/840841165544620062/843859541627764776/762971334774489111.png")
                embed.set_footer(text="Swagbucks Live")
                embed.timestamp = datetime.utcnow()
                sbm.send(embed=embed)
                hook.send(embed=embed)
            if message_data["code"] == 49:
                all_sb = []
                s = 0
                winners = message_data["winners"]
                for i in winners:
                    all_sb.append(i["sb"])
                    s = s + 1
                    if s == 20:
                        break
                sb = sorted(all_sb, reverse=True)
                sb = sb[0]
                embed = discord.Embed(title="**__Game Summary !__**", description=f"**• Payout : {sb}SB\n• Total Winners : {advancing}\n• Prize Money : ${prize_money()}**", color=discord.Colour.random())
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/840841165544620062/843859541627764776/762971334774489111.png")
                embed.set_footer(text="Swagbucks Live")
                embed.timestamp = datetime.utcnow()
                sbm.send(embed=embed)
                hook.send(embed=embed)


def get_auth_token():
    auth_token = BEARER_TOKEN
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
