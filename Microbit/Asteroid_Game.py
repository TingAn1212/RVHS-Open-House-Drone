import microbit

import random

class Shoot:
    def __init__(self,proj_cord):
        self.proj_cord = proj_cord
        self.proj_brightness = 5
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
        microbit.display.set_pixel(pixel.cord[0],pixel[1],brightness)

player = Player([2,4])
n = 0
var = True
var2 = True
asteriod = None
while True:
    n+=1
    lst = []
    if var2:
        player.shoot()
        var2 = False
    if microbit.button_a.was_pressed():
        player.move_left()
    if microbit.button_b.was_pressed():
        player.move_right()
    if not var2:
        if n%100 == 0:
            player.move_up()
        if player.check_hit(asteriod):
            var2 = True
            player.proj_cord = None
            var = True
        elif player.proj_cord[1] == -1:
            var2 = True
            player.proj_cord = None
        else:
            lst.append(player)
    
    
    if var:
        var = False
        asteriod = Asteriod([random.randint(0,4),0])
        lst.append(asteriod)
    if not var:
        if n%100 == 0:
            asteriod.move_down()
            if asteriod.cord[1]==5:
                asteriod = Asteriod([random.randint(0,4),0])
        lst.append(asteriod)
    if asteriod.check_crash(player):
        break
    microbit.display.clear()
    display(lst)
microbit.display.scroll("GAME OVER")