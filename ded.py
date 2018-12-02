import tgbot

last_update = 0

def process_update(update):
	

def check_updates():
	response = tgbot.get_updates_json(offset=last_update)['result']
	for update in response:
		if update['update_id'] >= last_update:
			last_update = update['update_id']
			process_update(update)


def main():
	update_id = tgbot.last_update(tgbot.get_updates_json())['update_id']
	while True:
		if update_id == tgbot.last_update(tgbot.get_updates_json())['update_id']:
			tgbot.send_message(tgbot.get_chat_id(tgbot.last_update(tgbot.get_updates_json())), 'test')
			update_id += 1

if __name__ == '__main__':
	main()