# Import kivy
from shutil import ExecError
from turtle import onrelease
from unittest.mock import MagicMixin
from kivy.app import App  
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.dropdown import DropDown
# from kivy.garden.joystick import Joystick

# Import drone
import threading 
import socket

#Global Variables
states = ""
local_address1 = ("",9000) 
local_address2 = ("0.0.0.0",8890) 
target_address = ('192.168.10.1', 8889)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(local_address1)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(local_address2)

#Info processing functions

#Async UDP functions
def state():
    global states
    print("Listening")
    while True:
        try:
            data, source = server.recvfrom(1518)
            states = data
        except Exception:
            print ('\nExit . . .\n')
            break
def recv():
    count = 0
    while True: 
        try:
            data, server = client.recvfrom(1518)
            print(data)
        except Exception:
            print ('\nExit . . .\n')
            break

# App classes
class Main(AnchorLayout):
    size_hint=1,1
    pass

class Stop(AnchorLayout):
    pass

class RoundedButton(Button):
    down = (0.25, 0.5, 1, 1)
    normal = (1, .2, .2, 1)
    def emergency(self):
        print("!!!!!!!!!!!")
        client.sendto(str.encode("emergency"), target_address)

class dropdown(DropDown):
    def send(self, cmd):
        try:
            print(cmd)
            client.sendto(str.encode(cmd), target_address)
            return "Ok"
        except Exception as e:
            return e

class FunctionsDropdown(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = dropdown()
        self.mainbutton = Button(text = "Functions", size_hint=(None, None), size=("120dp", "44dp"), pos_hint={"y":0})
        self.add_widget(self.mainbutton)
        self.mainbutton.bind(on_release = self.dropdown.open)

class DroneApp(App):
    pass

if __name__ == "__main__":
    #Init
    client.sendto(str.encode("command"), target_address)
    recvThread = threading.Thread(target=recv)
    recvThread.start()
    server.sendto(str.encode("command"), target_address)
    stateThread = threading.Thread(target=state)
    stateThread.start()

    # Running and closing server after closing app
    DroneApp().run()
    client.close() 
    server.close()