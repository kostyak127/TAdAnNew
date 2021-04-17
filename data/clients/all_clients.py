from telethon import TelegramClient
all_clients = list()

proxy_ip = 'proxy.digitalresistance.dog'
proxy_port = 443
secret = 'd41d8cd98f00b204e9800998ecf8427e'
proxy = (proxy_ip, proxy_port, secret)

a = TelegramClient('a', 2577630, '4b352a3071b0db69c363b4a252c9a73e', proxy=proxy)
all_clients.append(a)
