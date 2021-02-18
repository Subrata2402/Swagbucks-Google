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


webhook_url="https://discordapp.com/api/webhooks/805617639585480735/o6dKPMWro0o8mphA7iu3gB7ISNMP2gXS-4AVQu2n7V-1zVNm9NI2kDYAlFchpA87SgTG"

we="https://discordapp.com/api/webhooks/808873110233284679/cpufxGpBdyNoUb15Pelbw4P19bFAk5Qh2K_2GJLWRWPeDeGGJTJln9W3A1m3_FBYHlrp"


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
            x_in = x_ind.strftime("%d/%m/%Y")
            x_i = x_ind.strftime("%H:%M")
    
            prize = (response_data["nextShowPrize"])
            time.sleep(5)
            print(x_in)
            print(x_i)
            print(prize)
            #embed=discord.Embed(title=f"➜〢Date – {x_in}\n➜〢Time – {x_i}AM\n➜〢Prize Money – {prize}", color=0x00FBFF)
            #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775384878942257173/794110961333174293/1024x1024bb.png")
            #embed.set_footer(text="HQ Trivia Show | Subrata#3297")
            #hook.send(content="@everyone  **Next Game Details !**", embed=embed)



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
            print(message_data)

            if message_data['type'] == 'question':
                question = message_data['question']
                qcnt = message_data['questionNumber']
                Fullcnt = message_data['questionCount']

                print(f"\nQuestion number {qcnt} out of {Fullcnt}\n{question}")
                answers = [unidecode(ans["text"]) for ans in message_data["answers"]]
                print(f"\n{answers[0]}\n{answers[1]}\n{answers[2]}\n")
                real_question = str(question).replace(" ","+")
                google_query = "https://google.com/search?q="+real_question             
                embed=discord.Embed(title=f"**Question No. {qcnt} out of {Fullcnt}**",  description=f"**[{question}]({google_query})**", color=0xff5733)
                embed.add_field(name="**Option -１**", value=f"**[{answers[0]}]({google_query})**", inline=True)
                embed.add_field(name="**Option -２**", value=f"**[{answers[1]}]({google_query})**", inline=True)
                embed.add_field(name="**Option -３**", value=f"**[{answers[2]}]({google_query})**", inline=True)
                embed.set_footer(text="HQ Google | Subrata#3297", icon_url="")
                #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/578379566544846901/630400208265805835/401ec468afa82a2937b8ad3a4e811463.jpg")
                hook.send(embed=embed)
                hq.send(embed=embed)
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
                    embed2=discord.Embed(title=f"**__Google Search Results !__**", description=f"**１. {answers[0]}:** **{countoption1}** <:emoji_13:772843132093202443>\n**２. {answers[1]}:** **{countoption2}**\n**３. {answers[2]}:** **{countoption3}**", color=0x00FBFF)
                    embed2.set_footer(text="HQ Google | Subrata#3297")
                    hook.send(embed=embed2)
                    hq.send(embed=embed2)
                    #hook.send("dt")
                    sleep(10)
                    embed3=discord.Embed(title="⏰ Time's Up!", color=0x00FBFF) 
                    hook.send(embed=embed3)
                elif countoption2 == maxcount:
                    embed2=discord.Embed(title=f"**__Google Search Results !__**", description=f"**１. {answers[0]}:** **{countoption1}**\n**２. {answers[1]}:** **{countoption2}** <:emoji_13:772843132093202443>\n**３. {answers[2]}:** **{countoption3}**", color=0x00FBFF)
                    embed2.set_footer(text="HQ Google | Subrata#3297")
                    hook.send(embed=embed2)
                    hq.send(embed=embed2)
                    #hook.send("dt")
                    sleep(10)
                    embed3=discord.Embed(title="⏰ Time's Up!", color=0x00FBFF) 
                    hook.send(embed=embed3)
                else:
                    embed2=discord.Embed(title=f"**__Google Search Results !__**", description=f"**１. {answers[0]}:** **{countoption1}**\n**２. {answers[1]}:** **{countoption2}**\n**３. {answers[2]}:** **{countoption3}** <:emoji_13:772843132093202443>", color=0x00FBFF)
                    embed2.set_footer(text="HQ Google | Subrata#3297")
                    hook.send(embed=embed2)
                    hq.send(embed=embed2)
                    #hook.send("dt")
                    sleep(10)
                    embed3=discord.Embed(title="⏰ Time's Up!", color=0x00FBFF) 
                    hook.send(embed=embed3)

            elif message_data["type"] == "broadcastStats":
                connected = message_data["viewerCounts"]["connected"]
                playing = message_data["viewerCounts"]["playing"]
                watching = message_data["viewerCounts"]["watching"]
                advancing = message_data["roundCompleted"]
                eliminated = message_data["roundEliminated"]
                embed=discord.Embed(title="**__Answer Status !__**", description=f"**● Connected Players: {connected}\n● Playing: {playing}\n● Watching: {watching}\n● Advancing Players: {advancing}\n● Eliminated Players: {eliminated}**", color=0x00ffff)
                embed.set_footer(text="HQ Words | Subrata#3297")
                hook.send(embed=embed)

            elif message_data["type"] == "endRound":
                answer = message_data["answer"]
                hint = message_data["hint"]
                round_number = message_data["roundNumber"]
                total_round = message_data["totalRounds"]
                advancing = message_data["correctAnswers"]
                eliminated = message_data["incorrectAnswers"]
                letter = message_data["foundLetters"]
                embed=discord.Embed(title=f"**Round {round_number} out of {total_round}**", description=f"**● Correct Answer: {answer}\n● Hint: {hint}\n● Advancing Players: {advancing}\n● Eliminated Players: {eliminated}\n● Found Letters: {letter}**", color=0x00ffff)
                embed.set_footer(text="HQ Words | Subrata#3297")
                hook.send(embed=embed)


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
                ans = (5000)/(int(advancing))
                payout = float("{:.2f}".format(ans))
                total = int(advancing) + int(eliminated)
                percentAdvancing = (int(advancing)*(100))/(int(total))
                pA = float("{:.2f}".format(percentAdvancing))
                percentEliminated = (int(eliminated)*(100))/(int(total))
                pE = float("{:.2f}".format(percentEliminated))
                print(colored(correct, "blue"))
                print(advancing)
                print(eliminated)
                embd=discord.Embed(title=f"**__Answer Status !__**",  description=f"● **Correct Answer: {correct}** <:emoji_13:772843132093202443>\n**● Advancing Players: {advancing} ({pA}%)**\n**● Eliminated  Players: {eliminated} ({pE}%)**\n● **Current Payout: ${payout}**", color=0x4286f4)
                #embd.add_field(name="**__Status !__**", value=f"**● Advancing Players: {advancing} ({pA}%)**\n**● Eliminated  Players: {eliminated} ({pE}%)**", inline=True)
                embd.set_footer(text=f"HQ Google | Subrata#3297", icon_url="")
                hook.send(embed=embd)
                hq.send(embed=embd)

            elif message_data["type"] == "gameSummary":
                winn = message_data['numWinners']
                prizeMoney = str(message_data["winners"][0]["prize"])
                name1 = str(message_data["winners"][0]["name"])
                prize1 = str(message_data["winners"][0]["prize"])
                name2 = str(message_data["winners"][1]["name"])
                prize2 = str(message_data["winners"][1]["prize"])
                name3 = str(message_data["winners"][2]["name"])
                prize3 = str(message_data["winners"][2]["prize"])
                embed=discord.Embed(title="**__Game Summary !__**",description=f"**● Payout: {prizeMoney}\n● Total Winners: {winn}\n● Prize Money: $5,000**",color=0x00FBFF)
                embed.add_field(name="**__First Three Winners !__**", value=f"**● {name1} – {prize1}\n● {name2} – {prize2}\n● {name3} – {prize3}**")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737764195743039488/737768505935659178/giphy1.gif")
                embed.set_footer(text=f"HQ Google | Subrata#3297", icon_url="")
                hook.send(embed=embed)
                hq.send(embed=embed)




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
