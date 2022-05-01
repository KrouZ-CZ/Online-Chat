import json
import PySimpleGUI as sg
import socket
from cryptography.fernet import Fernet
import hashlib
import threading

sg.theme('default1')
layout1 = [
    [sg.Text('Enter login: '), sg.InputText(key='login')],
    [sg.Button('OK'), sg.Button('Exit', key='e1')]
]
layout2 = [
    [sg.Button('Create room')],
    [sg.Button('Connect to room')]
]
layout3 = [
    [sg.Text('Enter room name: '), sg.InputText(key='crn')],
    [sg.Text('Enter room password: '), sg.InputText(key='crp', password_char='*')],
    [sg.Button('Create'), sg.Button('Back', key='back1')]
]
layout4 = [
    [sg.Text('Enter room name: '), sg.InputText(key='corn')],
    [sg.Text('Enter room password: '), sg.InputText(key='corp', password_char='*')],
    [sg.Button('Connect'), sg.Button('Back', key='back2')]
]
layout5 = [
    [sg.Text('', key='Start')],
    [sg.Multiline(key='msgs', size=(50, 10), disabled=True)],
    [sg.InputText(key='text'), sg.Button('->')],
    [sg.Button('Back', key='back3'), sg.Button('Exit', key='e2')]
]
layout = [
    [sg.Column(layout1, visible=True, key='l1'), sg.Column(layout2, visible=False, key='l2'), sg.Column(layout3, visible=False, key='l3'), sg.Column(layout4, visible=False, key='l4'), sg.Column(layout5, visible=False, key='l5')]
]
window = sg.Window('Chat', layout)
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
encr = Encryptor()
class Chat:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 2000))
    def init(self, why):
        self.login = values['login']
        if why == 'Create':
            self.first = 'Create'
            self.roomname = values['crn']
            self.pwd = values['crp']
        elif why == 'Connect':
            self.first = 'Connect'
            self.roomname = values['corn']
            self.pwd = values['corp']
        window['Start'].update(f'Login: {self.login}\nRoomName: {self.roomname}')
        self.client.send(str([self.login, self.first, self.roomname, self.pwd]).encode('utf-8'))
        self.code = self.client.recv(1024).decode('utf-8')
        if self.code == 'Error':
            sg.Popup('Error')
            return 0
        window['l3'].update(visible=False)
        window['l4'].update(visible=False)
        window['l5'].update(visible=True)
        self.start()
    def start(self):
        lissen = threading.Thread(target=self.liss, args=())
        lissen.start()
    def send(self, text):
        self.client.send(encr.encrypt(text, self.pwd))
    def liss(self):
        self.send('Connected')
        self.msgs = ''
        while True:
            self.temp = self.client.recv(1024).decode('utf-8')
            if self.temp == 'Disconnect':
                break
            else:
                self.data = json.loads(self.temp.replace("'", '"'))
                self.msgs = f"{self.msgs}\n{self.data[0]}: {encr.decrypt(self.data[1], self.pwd)}"
                window['msgs'].update(self.msgs)
                window.refresh()
try:
    chat = Chat()
    pr = True
except:
    sg.Popup('Server closed')
    pr = False
while pr:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'e1' or event == 'e2':
        break
    elif event == 'OK':
        login = values['login']
        window['l1'].update(visible=False)
        window['l2'].update(visible=True)
    elif event == 'Create room':
        window['l2'].update(visible=False)
        window['l3'].update(visible=True)
    elif event == 'Connect to room':
        window['l2'].update(visible=False)
        window['l4'].update(visible=True)
    elif event == 'back1' or event == 'back2':
        window['l3'].update(visible=False)
        window['l4'].update(visible=False)
        window['l2'].update(visible=True)
    elif event == 'Create':
        chat.init('Create')
    elif event == 'Connect':
        chat.init('Connect')
    elif event == '->':
        chat.send(values['text'])
    elif event == 'back3':
        chat.client.send('Disconnect'.encode('utf-8'))
        window['l5'].update(visible=False)
        window['l2'].update(visible=True)
window.close()
