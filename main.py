from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, CardTransition
from kivy.config import Config
from datetime import date
from covid import Covid
from kivy.uix.boxlayout import BoxLayout


# Kivy window configuration
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'borderless', '1')
Config.write()


class DashboardScreen(Screen):
    pass

GUI  = Builder.load_file("main.kv")

class MainApp(App):

    def build(self):
        return GUI
    
    def on_start(self):
        pass

MainApp().run