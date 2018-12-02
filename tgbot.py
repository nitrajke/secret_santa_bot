import requests

url = "https://api.telegram.org/bot698720768:AAHiaeMXgoJBypUl_Xqb2gnRsFzGMGvW0jY/"
timeout = 30

def get_updates_json(offset=None):
	params = {'timeout': timeout, 'offset': offset}
	response = requests.get(url + 'getUpdates', data=params)
	return response.json()

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