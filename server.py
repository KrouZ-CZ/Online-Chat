import socket
import threading
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 2000))
server.listen(4)

rooms = {}

class User:
	def __init__(self, usr, adres):
		self.user = usr
		self.adres = adres
		self.start()
	def start(self):
		self.n = 0
		while True:
			while True:
				try:
					self.data = json.loads(self.user.recv(1024).decode('utf-8').replace("'", '"'))
				except:
					return
				if self.n == 1:
					self.user.send('Disconnect'.encode('utf-8'))
				if self.data[1] == 'Create':
					if self.data[2] in rooms:
						self.user.send('Error'.encode('utf-8'))
					else:
						self.user.send('Ok'.encode('utf-8'))
						rooms[self.data[2]] = {}
						rooms[self.data[2]]['pwd'] = self.data[3]
						rooms[self.data[2]]['users'] = [self.user]
						break
				else:
					if self.data[2] in rooms:
						if rooms[self.data[2]]['pwd'] == self.data[3]:
							rooms[self.data[2]]['users'].append(self.user)
							self.user.send('Ok'.encode('utf-8'))
							break
						else:
							self.user.send('Error'.encode('utf-8'))
					else:
						self.user.send('Error'.encode('utf-8'))
			print(f'Connected: {self.data[0]}')
			self.liss()
			self.n = 1
	def liss(self):
		try:
			while True:
				self.msgd = self.user.recv(1024).decode('utf-8')
				if self.msgd == 'Disconnect':
					print(f"Disconnected: {self.data[0]}")
					rooms[self.data[2]]['users'].remove(self.user)
					if len(rooms[self.data[2]]['users']) == 0:
						rooms.pop(self.data[2])
					break
				else:
					self.send(self.msgd)
		except:
			print(f"Disconnected: {self.data[0]}")
			rooms[self.data[2]]['users'].remove(self.user)
			try:
				if len(rooms[self.data[2]]['users']) == 0:
					rooms.pop(self.data[2])
			except:
				pass
	def send(self, msg):
		for usr in rooms[self.data[2]]['users']:
			try:
				usr.send(str([self.data[0], msg]).encode('utf-8'))
			except:
				print(f"Disconnected: {usr}")
				rooms[self.data[2]]['users'].remove(usr)
				try:
					if len(rooms[self.data[2]]['users']) == 0:
						rooms.pop(self.data[2])
				except:
					pass
def main():
	while True:
		user, adres = server.accept()
		t = threading.Thread(target=User, args=(user, adres))
		t.start()

if __name__ == '__main__':
	main()
