# Import kivy
from kivy.app import App  
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.dropdown import DropDown
from garden.joystick.joystick import Joystick
from kivy import platform
if platform == "android":
    from android.permissions import Permission, request_permissions
    request_permissions([Permission.INTERNET,Permission.ACCESS_NETWORK_STATE])
# Import drone
import threading 
import socket
from time import sleep

#Global Variables
states = ""
flag = {"stop":True}
coord = [[0,0],[0,0]]
local_address1 = ("",9000) 
local_address2 = ("0.0.0.0",8890) 
target_address = ('192.168.10.1', 8889)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(local_address1)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(local_address2)

#Info processing functions
def total(inp):
    res = 0
    for row in inp:
        for item in row:
            res += float(item)
    return res
#Async UDP functions
def state():
    global states
    while True:
        try:
            data, source = server.recvfrom(1518)
            states = str(data)
        except Exception:
            print ('\nExit . . .\n')
            break
def recv(tar):
    count = 0
    while True: 
        try:
            data, server = client.recvfrom(1518)
            count += 1
            tar.root.append(str(data))
        except Exception as e:
            print ('\nExit . . .\n')
            break
def move():
    while True:
        sleep(0.1)
        if (coord == "break"):
            break
        else:
            client.sendto(str.encode("rc {} {} {} {}".format(float(coord[0][0])*100,float(coord[0][1])*100,float(coord[1][1])*100,float(coord[1][0])*100)), target_address)
# App classes
class Main(AnchorLayout):
    size_hint=1,1
    def append(self,new):
        if new == "state":
            self.ids.console.tem_content.append(states + "\n") 
        else:
            self.ids.console.tem_content.append(new + "\n") 
        self.ids.console.update()

class Stop(AnchorLayout):
    pass

class Console(Label):
    tem_content = []
    content = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = self.convert(self.tem_content)
    def convert(self,inp):
        res = ""
        if len(self.tem_content) > 10:
            for row in inp[-10:]:
                res += row
        else:
            for row in inp:
                res += row
        if len(self.tem_content) > 15:
            inp.pop(0)
        return res

    def update(self):
        self.content = self.convert(self.tem_content)

class RoundedButton(Button):
    down = (0.25, 0.5, 1, 1)
    normal = (1, .2, .2, 1)
    def emergency(self):
        client.sendto(str.encode("emergency"), target_address)

class dropdown(DropDown):
    def send(self, cmd):
        try:
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

class Wasd(FloatLayout): #idk what to call it 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 20
        js = Joystick(pad_size = 0.4, outer_size = 0.4, inner_size=0.4, size_hint=(0.4,0.4))
        self.add_widget(js)
        js.bind(pad = self.update_coordinates)
    def update_coordinates(self, joystick, pad):
        x = str(pad[0])[0:5]
        y = str(pad[1])[0:5]
        radians = str(joystick.radians)[0:5]
        magnitude = str(joystick.magnitude)[0:5]
        angle = str(joystick.angle)[0:5]
        coord[0] = [x,y]

class Updown(FloatLayout): #idk what to call it x3
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 20
        ud = Joystick(pad_size = 0.4, outer_size = 0.4, inner_size=0.4, size_hint=(0.4,0.4), pos_hint={"right":1})
        self.add_widget(ud)
        ud.bind(pad = self.update_coordinates)
    def update_coordinates(self, joystick, pad):
        x = str(pad[0])[0:5]
        y = str(pad[1])[0:5]
        radians = str(joystick.radians)[0:5]
        magnitude = str(joystick.magnitude)[0:5]
        angle = str(joystick.angle)[0:5]
        coord[1] = [x,y]


class MainApp(App):
    pass

if __name__ == "__main__":
    #Init
    app = MainApp()
    client.sendto(str.encode("command"), target_address)
    recvThread = threading.Thread(target=recv,args=[app])
    recvThread.start()
    server.sendto(str.encode("command"), target_address)
    stateThread = threading.Thread(target=state)
    stateThread.start()
    moveThread = threading.Thread(target=move)
    moveThread.start()

    # Running and closing server after closing app
    app.run()
    client.close() 
    server.close()
    coord = "break"
    print("App closed successfully")