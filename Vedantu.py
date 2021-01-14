import discord
import requests
import json
import time
from lomond import WebSocket
from dhooks import Webhook, Embed
import websocket
from websocket import create_connection	

global question
question = None

btk = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI0MjQ0MjUwNzQzIiwiZXhwIjoxNjEyMjA4MTg3LCJpc3MiOiJ2ZWRhbnR1LmNvbSIsInNlc3Npb25EYXRhIjoie1wiZmlyc3ROYW1lXCI6XCJjaGV0YW5cIixcImxhc3ROYW1lXCI6XCJtYWRhcmphYXQgXCIsXCJmdWxsTmFtZVwiOlwiY2hldGFuIG1hZGFyamFhdFwiLFwidXNlcklkXCI6NDEwMjQ5ODUwNDQ2Nzc2NSxcInJvbGVcIjpcIlNUVURFTlRcIixcImNvbnRhY3ROdW1iZXJcIjpcIjQyNDQyNTA3NDNcIixcInBob25lQ29kZVwiOlwiMVwiLFwiY3JlYXRpb25UaW1lXCI6MTYwNzAyNDE4NzQ2MixcImV4cGlyeVRpbWVcIjoxNjEyMjA4MTg3NDYyLFwiaXNFbWFpbFZlcmlmaWVkXCI6ZmFsc2UsXCJpc0NvbnRhY3ROdW1iZXJWZXJpZmllZFwiOnRydWUsXCJpc0NvbnRhY3ROdW1iZXJETkRcIjpmYWxzZSxcImlzQ29udGFjdE51bWJlcldoaXRlbGlzdGVkXCI6ZmFsc2UsXCJyZWZlcnJhbENvZGVcIjpcImNoZXQ3MThhXCIsXCJ0bmNWZXJzaW9uXCI6XCJ2N1wiLFwiZGV2aWNlXCI6XCJXRUJcIixcImdyYWRlXCI6XCIxMlwiLFwiYm9hcmRcIjpcImlnY3NlXCIsXCJleGFtVGFyZ2V0c1wiOltcIk5FRVRcIl0sXCJ1c2VySW5Qcm9jZXNzT2ZPbmJvYXJkaW5nXCI6ZmFsc2UsXCJ0YXJnZXRcIjpcIk5FRVRcIixcInN0dWRlbnRJbmZvXCI6e1wiZ3JhZGVcIjpcIjEyXCIsXCJib2FyZFwiOlwiaWdjc2VcIixcInRhcmdldFwiOlwiTkVFVFwiLFwiZXhhbVRhcmdldHNcIjpbXCJORUVUXCJdLFwidXBkYXRlTmVlZGVkXCI6ZmFsc2V9fSJ9.dQZ8_87jd8STaQelEruA22zypbHL0zWGB7Hj_7Obtvk2QKyVCKfiT8DRBEmbyok-kUZVTVC08_TaN2NaczsF4w"


veda = "https://discord.com/api/webhooks/786474111420465162/wBrElahBp17Mo2BS1wti2beZb0iEtezi_qpSnQlJ1B-b0eAY7QuHqaf3Q5OPjj8QrwoW"

try:
	hook = Webhook(veda)
except:
	print('Invalid')



upcoming = 'https://vquiz.vedantu.com/dashboard/upcoming'

headers = {

	'method':'GET',
	'path' : '/dashboard/upcoming',
	'authority': 'vquiz.vedantu.com',
	'scheme':'https',
	'x-ved-token': btk,
	'accept-encoding':'gzip',
	'user-agent':'okhttp/3.14.4',

}

r = requests.get(url=upcoming, headers=headers).json()

data = r['result'][0]
gameId = data['_id']

sid_url = f'https://vquiz.vedantu.com/socket.io/?EIO=3&transport=polling&quizId={gameId}'

headers = {
	
	'method':'GET',
	'path':f'/socket.io/?EIO=3&transport=polling&quizId={gameId}',
	'authority':'vquiz.vedantu.com',
	'scheme':'https',
	'accept':'*/*',
	'x-ved-token': btk,
	'accept-encoding':'gzip',
	'user-agent':'okhttp/3.14.4',

}

r = requests.get(url=sid_url, headers=headers)

try:
	x = r.cookies
	c1 = 'AWSALB='+ x['AWSALB']
except:
	print('Cookie error')

try:
	rdata = r.text
	rdata = rdata[rdata.find('{'):]
	rjson = json.loads(rdata)
	SID = rjson["sid"]
except:
	print('SID Error...')

first = f'https://vquiz.vedantu.com/socket.io/?EIO=3&sid={SID}&transport=polling&quizId={gameId}'

headers = {
	
	'method':'GET',
	'path':f'/socket.io/?EIO=3&sid={SID}&transport=polling&quizId={gameId}',
	'authority':'vquiz.vedantu.com',
	'scheme':'https',
	'accept':'*/*',
	'x-ved-token': btk,
	'cookie':c1,
	'accept-encoding':'gzip',
	'user-agent':'okhttp/3.14.4',

}

r = requests.get(url=first, headers=headers)

try:
	x = r.cookies
	c1 = 'AWSALB='+ x['AWSALB']
except:
	print('Cookie error')

second = f'https://vquiz.vedantu.com/socket.io/?EIO=3&sid={SID}&transport=polling&quizId={gameId}'

headers = {
	
	'method':'GET',
	'path':f'/socket.io/?EIO=3&sid={SID}&transport=polling&quizId={gameId}',
	'authority':'vquiz.vedantu.com',
	'scheme':'https',
	'accept':'*/*',
	'x-ved-token': btk,
	'cookie':c1,
	'accept-encoding':'gzip',
	'user-agent':'okhttp/3.14.4',

}

r = requests.get(url=second, headers=headers)
print(r)

header = {
	
	'Upgrade':'websocket',
	'Connection':'Upgrade',
	'Sec-WebSocket-Key':'zKIu+BwuI++DC9+ZMBv4Ow==',
	'Sec-WebSocket-Version':'13',
	'X-Ved-Token': btk,
	'Cookie':c1,
	'Host':'vquiz.vedantu.com',
	'Accept-Encoding':'gzip',
	'User-Agent':'okhttp/3.14.4'
}

try:
	import thread
except ImportError:
	import _thread as thread
import time
def on_message(ws, message):
	if message == '3probe':
		print('Success')
	elif message != '3':
		try:
			message = message[message.find('['):]
			m = json.loads(message)
			mm = m[1]
			getType = mm['type']
			if getType == 'STATUS':
				try:
					qd = mm['metadata']
					qi = qd['current_question_index']
					qno = int(qi) + 1
					tq = qd['questions_count']
				except:
					print('Show not on')
			elif getType == 'QUESTION':
				global question
				question = mm['body']['newText']
				options = []
				order = []
				for i in mm['options']:
					options.append(i)
				opt1 = f'{options[0]}'
				opt2 = f'{options[1]}'
				opt3 = f'{options[2]}'
				for j in mm['optionOrder']:
					order.append(j)
				or1 = f'{order[0]}'
				or2 = f'{order[1]}'
				or3 = f'{order[2]}'
				rq = str(question).replace(' ','+')
				gq ="https://google.com/search?q="+rq
				if "not" in question:					
					embed = Embed(title=f'**Quiz Question [Not Question]**', description=f'[{question}]({gq})', color=0xFF6310)
					embed.add_field(name='**Option 1**', value=f'[{opt1}]({gq})')
					embed.add_field(name='**Option 2**', value=f'[{opt2}]({gq})')
					embed.add_field(name='**Option 3**', value=f'[{opt3}]({gq})')
					embed.set_footer(text="Vedantu Quiz | Made By Shivam#0123")
					hook.send(embed=embed)
				else:
					embed = Embed(title=f'**Quiz Question**', description=f'[{question}]({gq})', color=0xFF6310)
					embed.add_field(name='**Option 1**', value=f'[{opt1}]({gq})')
					embed.add_field(name='**Option 2**', value=f'[{opt2}]({gq})')
					embed.add_field(name='**Option 3**', value=f'[{opt3}]({gq})')
					embed.set_footer(text="Vedantu Quiz | Made By Shivam#0123")
					hook.send(embed=embed)
				r = requests.get('http://www.google.com/search?q=' + question)
				res = str(r.text)
				cnop1 = res.count(opt1)
				cnop2 = res.count(opt2)
				cnop3 = res.count(opt3)
				maxcount = max(cnop1, cnop2, cnop3)
				mincount = min(cnop1, cnop2, cnop3)
				if "not" in question:
					if cnop1 == mincount:
						embed = Embed(title="__Google Results!__", description=f"**1.{opt1} : {cnop1}**\n**2.{opt2} : {cnop2}** \n**3.{opt3} : {cnop3}**", color=0xFF6310)
						hook.send(embed=embed)
						hook.send('h')
						time.sleep(8)
						tm = Embed(title="**⏰ | Times Up!**",color=0x00F4FF)
						hook.send(embed=tm)
					elif cnop2 == mincount:
						embed = Embed(title="__Google Results!__", description=f"**1.{opt1} : {cnop1}** \n**2.{opt2} : {cnop2}**\n**3.{opt3} : {cnop3}**", color=0xFF6310)
						hook.send(embed=embed)
						hook.send('h')
						time.sleep(8)
						tm = Embed(title="**⏰ | Times Up!**",color=0x00F4FF)
						hook.send(embed=tm)
					else:
						embed = Embed(title="__Google Results!__", description=f"**1.{opt1} : {cnop1}**\n**2.{opt2} : {cnop2}**\n**3.{opt3} : {cnop3}**", color=0xFF6310)
						hook.send(embed=embed)
						hook.send('h')
						time.sleep(8)
						tm = Embed(title="**⏰ | Times Up!**",color=0x00F4FF)
						hook.send(embed=tm)
				else:
					if cnop1 == maxcount:
						embed = Embed(title="__Google Results!__", description=f"**1.{opt1} : {cnop1}**\n**2.{opt2} : {cnop2}**\n**3.{opt3} : {cnop3}**", color=0xFF6310)
						hook.send(embed=embed)
						hook.send('h')
						time.sleep(8)
						tm = Embed(title="**⏰ | Times Up!**",color=0x00F4FF)
						hook.send(embed=tm)
					elif cnop2 == maxcount:
						embed = Embed(title="__Google Results!__", description=f"**1.{opt1} : {cnop1}**\n**2.{opt2} : {cnop2}**\n**3.{opt3} : {cnop3}**", color=0xFF6310)
						hook.send(embed=embed)
						hook.send('h')
						time.sleep(8)
						tm = Embed(title="**⏰ | Times Up!**",color=0x00F4FF)
						hook.send(embed=tm)
					else:
						embed = Embed(title="__Google Results!__", description=f"**1.{opt1} : {cnop1}**\n**2.{opt2} : {cnop2}**\n**3.{opt3} : {cnop3}**", color=0xFF6310)
						hook.send(embed=embed)
						hook.send('h')
						time.sleep(8)
						tm = Embed(title="**⏰ | Times Up!**",color=0x00F4FF)
						hook.send(embed=tm)
			elif getType == 'SOLUTION':
				answer = mm['answer']
				ansNum = mm['answerNumber'][0]
				if ansNum == '1':
					embed = Embed(title=f"Question Summary", description=f"{question}", color=0x14FB00)
					embed.add_field(name="**Correct Answer :-**", value=f"Option {ansNum}.{answer}")
					hook.send(embed=embed)
				elif ansNum == '2':
					embed = Embed(title=f"Question Summary", description=f"{question}", color=0x14FB00)
					embed.add_field(name="**Correct Answer :-**", value=f"Option {ansNum}.{answer}")
					hook.send(embed=embed)
				else:
					embed = Embed(title=f"Question Summary", description=f"{question}", color=0x14FB00)
					embed.add_field(name="**Correct Answer :-**", value=f"Option {ansNum}.{answer}")
					hook.send(embed=embed)
			elif getType == 'WINNER':
				tw = mm['winnerCount']
				top = mm['totalParticpants']
				embed = Embed(title='**Quiz Summary !**',description=f"**• Total Winners : {tw}**\n**• Total Players Played : {top}**",color=0xFF6310)
				embed.set_footer(text="Vedantu Quiz | Made By Shivam#0123")
				hook.send(embed=embed)
	
		except:
			print(message)

def on_error(ws, error):
	print('Error')

def on_close(ws):
	print('Closed')

def on_open(ws):
	def run(*args):
		ws.send('2probe')
		ws.send('5')
		while True:
			try:
				time.sleep(15)
				ws.send('2')
			except:
				print('Unable to connect With Socket..')
				break
		time.sleep(1)
		ws.close()
		print('Thread Terminating..')
	thread.start_new_thread(run, ())


if __name__ == "__main__":
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp(f'wss://vquiz.vedantu.com/socket.io/?EIO=3&sid={SID}&transport=websocket&quizId={gameId}',
		                        on_message = on_message,
		                        on_error= on_error,
		                        on_close = on_close,
		                        cookie = c1,
		                        header = header)

	ws.on_open = on_open
	ws.run_forever()
