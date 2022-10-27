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

class Main(AnchorLayout):
    size_hint=1,1
    pass

class Stop(AnchorLayout):
    pass

class RoundedButton(Button):
    down = (0.25, 0.5, 1, 1)
    normal = (1, .2, .2, 1)

class dropdown(DropDown):
    pass

class FunctionsDropdown(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = DropDown()
        self.mainbutton = Button(text = "Functions", size_hint=(None, None), size=("120dp", "44dp"), pos_hint={"center_x": 0.5, "y":0})
        self.add_widget(self.mainbutton)
        self.mainbutton.bind(on_release = self.dropdown.open)

class WidgetApp(App):
    pass

WidgetApp().run()