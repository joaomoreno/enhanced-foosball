import requests
r = requests.post('https://67a1cb4d38d1.ngrok.io/api/game/start')
id = r.text

print(id)
r = requests.post('https://67a1cb4d38d1.ngrok.io/api/game/update', json = { 'ConversationId': id, 'Message': 'hello there' })
r = requests.post('https://67a1cb4d38d1.ngrok.io/api/game/update', json = { 'ConversationId': id, 'Message': 'hello there again' })
