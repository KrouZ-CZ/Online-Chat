import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 2000))
server.listen(4)

users = {}
rooms = {}

class User:
	def __init__(self, usr, adres):
		self.user = usr
		self.adres = adres
		users[usr] = self.user.recv(1024).decode('utf-8')
		self.passwd = self.user.recv(1024).decode('utf-8')
		if rooms.get(self.passwd) == None:
			rooms[self.passwd] = [self.user]
		else:
			rooms[self.passwd].append(self.user)
		print(f"Connected: {users[self.user]}/{adres}")
		for soct in rooms.get(self.passwd):
			soct.send(f'User {users.get(self.user)} connected'.encode('utf-8'))
		self.liss()
	def liss(self):
		try:
			while True:
				self.data = self.user.recv(1024).decode('utf-8')
				self.send(self.data)
		except:
			print(f"Disconnected: {users.get(self.user)}")
			rooms[self.passwd].remove(self.user)
			users.pop(self.user)
	def send(self, r):
		for soct in rooms.get(self.passwd):
			if soct == self.user: continue
			a = [users.get(self.user), str(r)]
			soct.send(str(a).encode('utf-8'))
def main():
	while True:
		user, adres = server.accept()
		t = threading.Thread(target=User, args=(user, adres))
		t.start()

if __name__ == '__main__':
	main()