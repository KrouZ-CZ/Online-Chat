import socket
import threading
import json
from cryptography.fernet import Fernet
import hashlib

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 2000))

name = input('Enter nick: ')
name = name if name != '' else 'User'
client.send(name.encode('utf-8'))

key = input('Enter password: ')
client.send(key.encode('utf-8'))

class Encryptor:
	def encrypt(self, text, key):
		password = hashlib.sha256(key.encode())
		f = Fernet(f'{password.hexdigest()[0:43]}=')
		encrypted_text = f.encrypt(text.encode())
		return encrypted_text
	def decrypt(self, text, key):
		password = hashlib.sha256(key.encode())
		f = Fernet(f'{password.hexdigest()[0:43]}=')
		encrypted_text = f.decrypt(text.encode())
		return str(encrypted_text)[2:-1]
Encr = Encryptor()
def liss():
	while True:
		listen = client.recv(1024).decode('utf-8')
		with open('test.txt', 'w') as file: file.write(listen)
		if listen[0:4] == 'User':
			print(f'\r{listen}\n{name}: ', end='')
		else:
			sort = json.loads(listen.replace("'", '"'))
			print(f'\r{sort[0]}: {Encr.decrypt(sort[1], key)}\n{name}: ', end='')
t = threading.Thread(target=liss, args=())
t.start()
while True:
	a = input("{}: ".format(name))
	client.send(Encr.encrypt(a, key))