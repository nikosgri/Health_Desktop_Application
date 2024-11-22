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
from kivy.animation import Animation
from bar import Bar


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
        self.today = date.today()
        self.date = self.today.strftime('%B %D %Y')
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

        self.root.ids['dashboard_screen'].ids['date_label_id'].text = self.date 

        self.covid = Covid(source="worldometers")

    
    def close(self):
        quit()
    
    def minimize(self):
        Window.minimize()

    def process_datasearch(self):
        _location = (self.root.ids['dashboard_screen'].ids['search_location_id'].text).strip()
        print("Location:", _location)
        try:
            _data = self.covid.get_status_by_country_name(_location)
            #cases
            self.root.ids['dashboard_screen'].ids['confirmed_cases_id'].text = (f"{(_data['confirmed']):,d}")
            self.root.ids['dashboard_screen'].ids['confirmed_cases_delta_id'].text = (f"{(_data['new_cases']):,d}")
            self.root.ids['dashboard_screen'].ids['confirmed_deaths_id'].text = (f"{(_data['deaths']):,d}")
            self.root.ids['dashboard_screen'].ids['confirmed_deaths_delta_id'].text = (f"{(_data['new_deaths']):,d}")
            self.root.ids['dashboard_screen'].ids['recovered_cases_id'].text = (f"{(_data['recovered']):,d}")
            self.root.ids['dashboard_screen'].ids['active_cases_id'].text = (f"{(_data['active']):,d}")

            #Recovery rate
            recovery_rate = (_data['recovered']/_data['confirmed'])*100
            self.root.ids['dashboard_screen'].ids['recovery_rate_id'].text = str(int(recovery_rate)) + "% of cases\n recovered"
            self.root.ids['dashboard_screen'].ids['critical_cases_id'].text = str((f"{(_data['critical']):,d}")) + " cases in\n critical state"
        except:
            print("Location",_location,"doesn't exist")

MainApp().run()
