from kivy.app import App  
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
# from kivy.garden.joystick import Joystick
 
class WidgetApp(App):
    pass
class RoundedButton(Button):
    down = (0.25, 0.5, 1, 1)
    normal = (1, .2, .2, 1)

WidgetApp().run()