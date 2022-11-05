import microbit
from time import sleep
import random

class Shoot:
    def __init__(self,proj_cord):
        self.proj_cord = proj_cord
        self.proj_brightness = 7
    def move_up(self):
        self.proj_cord = [self.proj_cord[0],self.proj_cord[1]-1]
    def check_hit(self,asteriod):
        if asteriod == None:
            return False
        if asteriod.cord == self.proj_cord:
            return True
        else:
            return False
        
class Player(Shoot):
    def __init__(self,cord):
        self.name = "player"
        self.cord = cord
        self.proj_cord = None
        self.brightness = 9
    def move_left(self):
        if self.cord[0] == 0:
            pass
        else:
            self.cord = [self.cord[0]-1,self.cord[1]]
    def move_right(self):
        if self.cord[0] == 4:
            pass
        else:
            self.cord = [self.cord[0]+1,self.cord[1]]
    def shoot(self):
        super().__init__([self.cord[0],self.cord[1]-1])
        

class Asteriod:
    def __init__(self,cord):
        self.name = "asteriod"
        self.cord = cord
        self.brightness = 9
    def move_down(self):
        self.cord = [self.cord[0],self.cord[1]+1]
    def check_crash(self,player):
        if player.cord == self.cord:
            return True
        else:
            return False
        
def display(pixels,brightness = 9):
    for pixel in pixels:
        if pixel.cord[1] < 5:
            microbit.display.set_pixel(pixel.cord[0],pixel.cord[1],brightness)

player = Player([2,4])
n = 0
var = True
var2 = True
asteriod = None
lst = []
lst.append(player)
while True:
    sleep(0.02)
    n+=1
    if n > 10:
        n = 0
    if microbit.button_a.was_pressed():
        player.move_left()
    if microbit.button_b.was_pressed():
        player.move_right()
    # if not var2:
    #     if player.check_hit(asteriod):
    #         var2 = True
    #         player.proj_cord = None
    #         var = True
    #     elif player.proj_cord[1] == -1:
    #         var2 = True
    #         player.proj_cord = None
    #     else:
    
    if var:
        var = False
    if not var:
        if n == 10:
            for item in lst:
                if item.name == "asteriod":
                    item.move_down()
            if random.choice([1,2,3,4,5]) < 3:
                lst.append(Asteriod([random.randint(0,4),0]))
    b = False
    for item in lst:
        if item.name == "asteriod":
            if item.check_crash(player):
                b = True
                break
            if item.cord[1] > 5:
                lst.remove(item)
    microbit.display.clear()
    display(lst)
    if b:
        break
microbit.display.scroll("GAME OVER")