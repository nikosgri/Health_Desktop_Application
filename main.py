from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.uix.button import ButtonBehavior,Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen,NoTransition,CardTransition
from kivy.config import Config
from datetime import date
from covid import Covid
from kivy.uix.boxlayout import BoxLayout

Config.set('graphics','width','1200')
Config.set('graphics', 'height','900')
Config.set('graphics','borderless','1')
Config.write()

class ImageButton(ButtonBehavior, Image):
    pass

class LabelButton(ButtonBehavior, Label):
    pass

class Spacer(Label):
    pass

class DashboardScreen(Screen):
    pass


# Load the main file to builder
GUI = Builder.load_file("main.kv") 

class MainApp(App):

    def build(self):
        return GUI
    
    def on_start(self):
        #Pass the fonts to the UI
        LabelBase.register(name = 'myraid_pro_reg', fn_regular = 'MYRIADPRO-CONDIT.OTF')
        LabelBase.register(name = 'd_din_reg', fn_regular = 'd-din.regular.ttf')
        LabelBase.register(name = 'roboto-medium', fn_regular = 'Roboto-Medium.ttf')
        LabelBase.register(name = 'roboto-thin', fn_regular = 'Roboto-Thin.ttf')
        LabelBase.register(name = 'bistecca', fn_regular = 'Bistecca.ttf')
        LabelBase.register(name = 'teko-reg', fn_regular = 'Teko-Regular.ttf')
        LabelBase.register(name = 'barlow-reg', fn_regular = 'BarlowSemiCondensed-Regular.ttf')
        LabelBase.register(name = 'barlow-bold', fn_regular = 'BarlowSemiCondensed-SemiBold.ttf')

    
    def close(self):
        quit()
    
    def minimize(self):
        Window.minimize()

MainApp().run()
