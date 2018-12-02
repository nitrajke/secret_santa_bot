import requests

url = "https://api.telegram.org/bot698720768:AAHiaeMXgoJBypUl_Xqb2gnRsFzGMGvW0jY/"
timeout = 10
answer = 0

def log(response):
	fname = str(answer) + '.html'
	f = open(fname, 'w')
	f.write(response.text)
	f.close()
	answer += 1

def get_updates_json(offset=None):
	global answer
	params = {'timeout': timeout, 'offset': offset}
	response = requests.get(url + 'getUpdates', data=params)
	log(response)
	return response.json()

def get_chat_members_count(chat_id):
	params = {'chat_id': chat_id}
	response = requests.get(url + 'getChatMembersCount', data=params)
	log(response)
	return int(response.json()['result'])

def last_update(data):
	results = data['result']
	total_updates = len(results) - 1
	return results[total_updates]

def get_chat_id(update):
	chat_id = update['message']['chat']['id']
	return chat_id

def send_message(chat, text):
	params = {'chat_id': chat, 'text': text}
	response = requests.post(url + 'sendMessage', data=params)
	return response