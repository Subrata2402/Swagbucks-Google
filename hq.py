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


webhook_url="https://discordapp.com/api/webhooks/739231985959960697/l9o4LfiZdWOqzXhbpUriEOo25EbjAIicujboN_yGyHkzWe3c9cH0i_ILVHMcwn9f0Gyt"

we="https://discordapp.com/api/webhooks/739231985959960697/l9o4LfiZdWOqzXhbpUriEOo25EbjAIicujboN_yGyHkzWe3c9cH0i_ILVHMcwn9f0Gyt"


try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")


try:
    hq = Webhook(we)
except:
    print("Invalid WebHook Url Lol")
    

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
            tim = (response_data["nextShowTime"])
            tm = aniso8601.parse_datetime(tim)
            x =  tm.strftime("%H:%M:%S [%d/%m/%Y] ")
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            x_in = x_ind.strftime("%H:%M:%S [%d/%m/%Y] ")
    
            prize = (response_data["nextShowPrize"])
            time.sleep(5)
            print(x_in)
            print(prize)
            embed = Embed(title=f"HQ Trivia", description=f"**Next Game Starts In**\n**{x_in}**", color=0x000000)
            embed.add_field(name="Next Show Prize", value=f"**{prize}**",inline=True)
            embed.set_image(url="https://cdn.discordapp.com/attachments/649457795875209265/672845602824126494/Nitro_2.gif")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/578379566544846901/630400208265805835/401ec468afa82a2937b8ad3a4e811463.jpg")
            embed.set_footer(text="HQ Google")
            embed.timestamp = (datetime.datetime.utcnow())
            hook.send(content="**Connected To Hq Websocket**✅",embed=embed)



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
           # print(message_data)

            if message_data['type'] == 'question':
                question = message_data['question']
                qcnt = message_data['questionNumber']
                Fullcnt = message_data['questionCount']

                print(f"\nQuestion number {qcnt} out of {Fullcnt}\n{question}")
                answers = [unidecode(ans["text"]) for ans in message_data["answers"]]
                print(f"\n{answers[0]}\n{answers[1]}\n{answers[2]}\n")
                real_question = str(question).replace(" ","+")
                google_query = "https://google.com/search?q="+real_question             
                embed=discord.Embed(title=f"Question {qcnt}/{Fullcnt}",description=f"**{qcnt}.** {question}\n**Option 1**\n{answers[0]}\n**Option 2**\n{answers[1]}\n**Option 3**\n{answers[2]}", color=0x00ff00)
                embed.set_footer(text="Made By Akhil")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/578379566544846901/630400208265805835/401ec468afa82a2937b8ad3a4e811463.jpg")
                hook.send(embed=embed)
                #hook.send("+hp")
                option1=f"{answers[0]}"
                option2=f"{answers[1]}"
                option3=f"{answers[2]}"
                r = requests.get("http://google.co.in/search?q=" + question + option1 + option2 + option3)
                soup = BeautifulSoup(r.text, 'html.parser')
                response = soup.find_all("span", class_="st")
                res = str(r.text)
                countoption1 = res.count(option1)
                countoption2 = res.count(option2)
                countoption3 = res.count(option3)
                maxcount = max(countoption1, countoption2, countoption3)
                sumcount = countoption1+countoption2+countoption3
                print("/n")
                if countoption1 == maxcount:
                	print(f"A {answers[0]}")
                elif countoption2 == maxcount:
                	print(f"B {answers[1]}")
                else:
                	print(f"C {answers[2]}")              
                if countoption1 == maxcount:
                    embed2=discord.Embed(title=f"Question {qcnt}/12",description=f"{question}\n\n**Google Results:**\n**➊.{answers[0]}:** **{countoption1}**✅ \n**➋.{answers[1]}:** **{countoption2}**\n**➌.{answers[2]}:** **{countoption3}**")
                    embed2.set_footer(text="Made By ⚘!ϻ.Captainᴼᴾ")
                    hook.send(embed=embed2)
                    #hook.send("hq")
                elif countoption2 == maxcount:
                    embed2=discord.Embed(title=f"Question {qcnt}/12",description=f"{question}\n\n**Google Results:**\n**➊.{answers[0]}:** **{countoption1}** \n**➋.{answers[1]}:** **{countoption2}** ✅ \n**➌.{answers[2]}:** **{countoption3}**")
                    embed2.set_footer(text="Made By ⚘!ϻ.Captainᴼᴾ")
                    hook.send(embed=embed2)
                    #hook.send("hq")
                else:
                    embed2=discord.Embed(title=f"Question {qcnt}/12",description=f"{question}\n\n**Google Results:**\n**➊.{answers[0]}:** **{countoption1}**\n**➋.{answers[1]}:** **{countoption2}**\n**➌.{answers[2]}:** **{countoption1}**✅")
                    embed2.set_footer(text="Made By ⚘!ϻ.Captainᴼᴾ")
                    hook.send(embed=embed2)
                    #hook.send("hq")
                    
            elif message_data["type"] == "questionSummary":

                answer_counts = {}
                correct = ""
                for answer in message_data["answerCounts"]:
                    ans_str = unidecode(answer["answer"])

                    if answer["correct"]:
                        correct = ans_str
                advancing = message_data['advancingPlayersCount']
                eliminated = message_data['eliminatedPlayersCount']
                nextcheck = message_data['nextCheckpointIn']

                print(colored(correct, "blue"))
                print(advancing)
                print(eliminated)
                embd=discord.Embed(title="Answer Stats",description=f"**Correct Answer : {correct} ✅** ",color=0x00ff00)
                embd.add_field(name=f"Advancing Players:",value=f"**{advancing} **",inline=True)
                embd.add_field(name=f"Eliminated  Players:",value=f"**{eliminated} **",inline=True)
                embd.set_thumbnail(url="")
                embd.set_footer(text=f"Made By ⚘!ϻ.Captainᴼᴾ")
                hook.send(embed=embd)

            elif message_data["type"] == "gameSummary":
                winn = message_data['numWinners']
                prizeMoney = str(message_data["winners"][0]["prize"])
                embed=discord.Embed(title="**Game Summary**",description="",color=0x00FBFF)
                embed.add_field(name="**� Payout:**", value=f"**{prizeMoney}**", inline=True)
                embed.add_field(name="**� Total Winners :**", value=f"**{winn} 🎉**", inline=True)
               # embed.add_field(name="**� Prize Money :**", value=f"**5000$**", inline=True)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737764195743039488/737768505935659178/giphy1.gif")
                embed.set_footer(text=f"Made By ⚘!ϻ.Captainᴼᴾ")
                hook.send(embed=embed)




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
