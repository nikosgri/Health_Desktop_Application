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
from kivy.uix.boxlayout import BoxLayout

Config.set('graphics','width','1200')
Config.set('graphics', 'height','900')
Config.set('graphics','borderless','1')
Config.write()

import kivy.utils

class LocationBarItem(BoxLayout):
    def __init__(self,**kwargs):
        self.orientation = "horizontal"
        self.size_hint= (0.74,1)
        super().__init__()

        bar_item = BoxButton(orientation="vertical",size_hint=(0.01,0.9))
        _bar = Bar(size_hint=(1,0.9),value = kwargs['cases'])
        _loc = Label(size_hint=(1,0.1), text=kwargs['loc'], font_size="10sp", color=kivy.utils.get_color_from_hex("#4746e"))
        bar_item.add_widget(_bar)
        bar_item.add_widget(_loc)
        self.add_widget(bar_item)

# START OF WIDGETS
class BoxButton(ButtonBehavior, BoxLayout):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class LabelButton(ButtonBehavior, Label):
    pass

class Spacer(Label):
    pass

class DashboardScreen(Screen):
    pass
# END OF WIDGETS

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
        cases_plot = self.root.ids['dashboard_screen'].ids['cases_plot_id']
        self.covid = Covid(source="worldometers")

        chart_countries ={
        "ZA" : "South Africa",
        "NE":"Nigeria",
        "GH":"Ghana",
        "KE":"Kenya",
        "SN":"Senegal",
        "GN":"Guinea",
        "EG":"Egypt",
        "TG":"Togo",
        "ZM":"Zambia",
        "US":"USA",
        "MX":"Mexico",
        "CA":"Canada",
        "PA":"Panama",
        "HT":"Haiti",
        "CU":"Cuba",
        "JM":"Jamaica",
        "HN":"Honduras",
        "CR":"Costa Rica",
        "NI":"Nicaragua",
        "BR":"Brazil",
        "PE":"Peru",
        "CO":"Colombia",
        "CL":"Chile",
        "AR":"Argentina",
        "VE":"Venezuela",
        "GY":"Guyana",
        "BO":"Bolivia",
        "EC":"Ecuador",
        "UY":"Uruguay",
        "IN":"India",
        "IR":"Iran",
        "SA":"Saudi Arabia",
        "BD":"Bangladesh",
        "PK":"Pakistan",
        "TR":"Turkey",
        "IQ":"Iraq",
        "IL":"Israel",
        "CN":"China",
        "TW":"Taiwan",
        "RU":"Russia",
        "ES":"Spain",
        "UK":"UK",
        "FR":"France",
        "IT":"Italy",
        "DE":"Germany",
        "GR":"Greece",
        "RS":"Serbia",
        "NO":"Norway",
        "AL":"Albania",
        "AU":"Australia",
        "NZ":"New Zealand",
        "FJ":"Fiji",
        "JP":"Japan",
        "PT":"Portugal",
        "SD":"Sudan",
        "BF":"Burkina Faso",
        "SG":"Singapore"}



        countries_short ={

        "CO":"Colombia",
        "MX":"Mexico",
        "ES":"Spain",
        "CL":"Chile",
        "AR":"Argentina",
        "IR":"Iran",
        "UK":"UK",
        "SA":"Saudi Arabia",
        "BD":"Bangladesh",
        "PK":"Pakistan",
        "FR":"France",
        "TR":"Turkey",
        "IT":"Italy",
        "IQ":"Iraq",
        "CA":"Canada",
        "BO":"Bolivia",
        "IL":"Israel",
        "EG":"Egypt",
        "PA":"Panama",
        "CN":"China",
        "JP":"Japan",
        "PT":"Portugal",
        "SG":"Singapore",
        "NE":"Nigeria",
        "GH":"Ghana",
        "CR":"Costa Rica",
        "KE":"Kenya",
        "RS":"Serbia",
        "AU":"Australia",
        "ZM":"Zambia",
        "NO":"Norway",
        "GR":"Greece",
        "GN":"Guinea",
        "HT":"Haiti"

        }

        temp_json = self.covid.get_status_by_country_name("Colombia")
        CO_cases = temp_json['confirmed']

        for key, value in countries_short.items():
            location_case = self.covid.get_status_by_country_name(value)
            normalized_value = min(int((location_case['confirmed'] / CO_cases) * 100), 100)
            location_bar_item = LocationBarItem(loc=str(key),cases= normalized_value)
            cases_plot .add_widget(location_bar_item)

    
    def close(self):
        quit()
    
    def minimize(self):
        Window.minimize()

    def process_datasearch(self):
        error_msg = "This location does not exist,\n please check the spelling."
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
            self.root.ids['dashboard_screen'].ids['error_message_id'].text = ""
        except:
            self.root.ids['dashboard_screen'].ids['error_message_id'].text = error_msg

MainApp().run()
