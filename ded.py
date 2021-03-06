#!/usr/bin/env python3
#
import tgbot
import random
from time import sleep

random.seed()

timeout = 3

last_update = 0
groups = { }

def send_results(group_id):
	for player in groups[group_id]['members']:
		text = 'Дари подарок этому человеку: ' + groups[group_id]['members'][player]['first_name'] + ' ' + groups[group_id]['members'][player]['last_name'] + '!'
		chat_id = groups[group_id]['members'][player]['secret_santa_chat_id']
		tgbot.send_message(chat_id, text)

def play(chat_id):
	free_santas = list(groups[chat_id]['members'].keys())
	free_victims = free_santas[:]
	players = {x: None for x in free_santas}
	while len(free_santas) > 0:
		if len(free_santas) == 2:
			if free_santas[0] in free_victims:
				if free_santas[0] == free_victims[0]:
					players[free_santas[0]] = free_victims[1]
					players[free_santas[1]] = free_victims[0]
					break
				else:
					players[free_santas[0]] = free_victims[0]
					players[free_santas[1]] = free_victims[1]
					break
			elif free_santas[1] in free_victims:
				if free_santas[1] == free_victims[0]:
					players[free_santas[0]] = free_victims[0]
					players[free_santas[1]] = free_victims[1]
					break
				else:
					players[free_santas[0]] = free_victims[1]
					players[free_santas[1]] = free_victims[0]
					break

		pls = free_victims[:]
		if free_santas[len(free_santas) - 1] in pls:
			pls.remove(free_santas[len(free_santas) - 1])
		player = random.choice(pls)
		players[free_santas[len(free_santas) - 1]] = player

		free_victims.remove(player)
		free_santas.pop()
	for member in players:
		groups[chat_id]['members'][member]['secret_santa_chat_id'] = players[member]
	send_results(chat_id)

def process_update(update):

	if 'message' in update and 'text' in update['message']:
		chat_id = str(update['message']['chat']['id'])
		text = update['message']['text']

		if update['message']['chat']['type'] == 'private':
			splited_text = text.split(' ')
			if '/start' in splited_text:
				if len(splited_text) > 1 and splited_text[1] in groups and not chat_id in groups[splited_text[1]]['members']:
					groups[splited_text[1]]['members'][chat_id] = {}
					groups[splited_text[1]]['members'][chat_id]['id'] = chat_id
					groups[splited_text[1]]['members'][chat_id]['secret_santa_chat_id'] = None
					groups[splited_text[1]]['members'][chat_id]['first_name'] = update['message']['from']['first_name']
					try:
						groups[splited_text[1]]['members'][chat_id]['last_name'] = update['message']['from']['last_name']
					except:
						groups[splited_text[1]]['members'][chat_id]['last_name'] = ''
					try:
						groups[splited_text[1]]['members'][chat_id]['username'] = update['message']['from']['username']
					except:
						groups[splited_text[1]]['members'][chat_id]['username'] = ''
					vacancies_count = groups[splited_text[1]]['members_count'] - len(groups[splited_text[1]]['members'])
					msg = groups[splited_text[1]]['members'][chat_id]['first_name'] + ' ' + groups[splited_text[1]]['members'][chat_id]['last_name'] + ' участвует. Осталось мест: ' + str(vacancies_count)
					if groups[splited_text[1]]['members'][chat_id]['username'] == 'tfent':
						msg = 'Я - хороший дедушка мороз. Но вынужден сообщить прискорбные известия: Роман тоже участвует. Кто вообще его позвал? :( Эххх... Осталось мест: ' + str(vacancies_count)
					tgbot.send_message(splited_text[1], msg)
				else:
					tgbot.send_message(chat_id, 'Странно, такого быть не должно. Скорее всего Роман что-то сломал. Маякните Мишгану. Код : 01')
			else:
				tgbot.send_message(chat_id, 'Странно, такого быть не должно. Скорее всего Роман что-то сломал. Маякните Мишгану. Код : 02')

		elif (update['message']['chat']['type'] == 'group' or
			update['message']['chat']['type'] == 'supergroup'):
			if text == '/start@TayniyDedBot' and not chat_id in groups:
				groups[chat_id] = {}
				groups[chat_id]['id'] = chat_id
				groups[chat_id]['title'] = update['message']['chat']['title']
				groups[chat_id]['members_count'] = tgbot.get_chat_members_count(chat_id) - 1 # 1 - self
				groups[chat_id]['members'] = {}
				click_url = 'https://t.me/TayniyDedBot?start=' + chat_id
				tgbot.send_message(chat_id, 'Кликните ссылку и в открывшемся чате нажмите start. ' + click_url)
			elif text == '/reset@TayniyDedBot' and chat_id in groups:
				groups.pop(chat_id)
			elif text == '/play@TayniyDedBot' and chat_id in groups:
				if (groups[chat_id]['members_count'] - len(groups[chat_id]['members'])) == 0:
					tgbot.send_message(chat_id, '*играет_новогодняя_мелодия*')
					play(chat_id)
				else:
					tgbot.send_message(chat_id, 'Рано. Еще есть вакантные места.')
		else: #channel
			pass

def check_updates():
	global last_update
	response = tgbot.get_updates_json(offset=last_update)['result']
	for update in response:
		if update['update_id'] >= last_update:
			last_update = update['update_id'] + 1
			print(last_update)
			process_update(update)


def main():
	while True:
		check_updates()
		sleep(timeout)

if __name__ == '__main__':
	main()