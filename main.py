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
# Import drone
from plyer import stt, spatialorientation
from math import pi
import threading 
import socket
from time import sleep
from kivy.clock import Clock
if platform == "android":
    spatialorientation.enable_listener()
    from android.permissions import Permission, request_permissions
    request_permissions([Permission.INTERNET,Permission.ACCESS_NETWORK_STATE,Permission.RECORD_AUDIO])
#Global Variables
states = ""
flag = {"stop":True,"lock":False}
coord = [[0,0],[0,0]]
local_address1 = ("",9000) 
local_address2 = ("0.0.0.0",8890) 
target_address = ('192.168.10.1', 8889)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(local_address1)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(local_address2)
stt.language = "en-US"

#Info processing functions
def total(inp):
    res = 0
    for row in inp:
        for item in row:
            res += float(item)
    return res
def include(source,target):
    for item in target:
        if item in source or item.lower() in source:
            return True
    return False
def read(target):
    target = target.split("'")[1]
    result = {"dict":True}
    tem = target.split(";")
    for item in tem:
        if ":" in item:
            tempo = item.split(":")
            result[tempo[0]] = tempo[1]
    return result
def degree(src):
    res = []
    for item in src:
        tem = float(item)/pi*180
        if tem < 0:
            #tem = 180 + (-1*tem)
            pass
        res.append(round(tem,2))
    return res
def close(i1,i2,range):
    return abs(i1-i2) < range
#Async UDP functions
def state():
    global states
    while True:
        try:
            data, source = server.recvfrom(1518)
            states = str(data)
        except Exception as e:
            #print(e)
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
            #print(e)
            print ('\nExit . . .\n')
            break
def move():
    while True:
        sleep(0.1)
        if (coord == "break"):
            break
        else:
            if not flag["lock"]:
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
        if len(self.tem_content) > 5:
            for row in inp[-5:]:
                res += row
        else:
            for row in inp:
                res += row
        if len(self.tem_content) > 7:
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
    def sync(self):
        yaw = 0
        try:
            yaw = int(read(states)["yaw"])
        except:
            pass
        ori = degree(spatialorientation.orientation)
        ori[0] += 90
        if ori[0] > 180:
            ori[0] = (ori[0]-180) + -180
        if not close(yaw,ori[0],10) and platform == "android":
            flag["lock"] = True
            ind = 0
            respond = "Error"
            self.send("rc 0 0 0 100")
            while (ind < 60):
                sleep(0.1)
                ind += 1
                yaw = int(read(states)["yaw"])
                if close(yaw,ori[0],10):
                    respond = "ok"
                    self.send("rc 0 0 0 0")
                    break
            flag["lock"] = False
            app.root.append(respond)
        app.root.append(str(ori))
        
    def send(self, cmd):
        try:
            client.sendto(str.encode(cmd), target_address)
            return "Ok"
        except Exception as e:
            return e
            
    def listen(self):
        if stt.listening:
            self.stop_listening()
            return 
        start_button = self.ids.start_button
        start_button.text = 'Stop'

        stt.start()
        #audio.start()

        Clock.schedule_interval(self.check_state, 1 / 5)

    def stop_listening(self):
        start_button = self.ids.start_button
        start_button.text = 'Start Listening'

        stt.stop()
        #audio.stop()
        self.update()

        Clock.unschedule(self.check_state)
    
    def check_state(self, dt):
        print(stt.listening)
        if not stt.listening:
            print(stt.errors)
            self.stop_listening()

    def update(self):
        print(stt.results)
        print(stt.partial_results)
        #audio.play()
        result = stt.results
        if (include(result,["TAKE OFF","TAKE","TAKE ALL","TAKEOFF"])):
            app.root.append("takeoff")
            self.send("takeoff")
        elif (include(result,["LAND","LEND","LEARN","LEAN","LET"])):
            app.root.append("land")
            self.send("land")
        elif (include(result,["SLEEP","SHEEP","FLIP","FREE","ZIP"])):
            app.root.append("flip")
            self.send("flip b")
        else:
            app.root.append(str(result))


class FunctionsDropdown(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = dropdown()
        self.mainbutton = Button(text = "Functions", size_hint=(None, None), size=("120dp", "44dp"), pos_hint={"y":0})
        self.add_widget(self.mainbutton)
        self.mainbutton.bind(on_release = self.dropdown.open)

class Wasd(FloatLayout): 
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

class Updown(FloatLayout):
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