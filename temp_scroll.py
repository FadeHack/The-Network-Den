from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty, ReferenceListProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import psutil
from threading import Thread
import functools
from kivy.uix.image import Image
import requests
from kivy.config import Config
Config.set('graphics', 'resizable', True)


global networkInterfaces
# global api_uri
# api_uri = "http://127.0.0.1:5000/saveascsv"
addrs = psutil.net_if_addrs() 
networkInterfaces = list(addrs.keys())


class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class SecondOneWindow(Screen):
    def build(self):
        self.my_spinner = ObjectProperty()
    
    def sendData(self,send_data):
        print(send_data)
        header = {"Content-type":"application/json"}

        response = requests.post("http://127.0.0.1:5000/saveascsv",json = send_data, headers = header)
        print(response.content)
            
    def pressed(self):
        networkInterface = self.ids.my_spinner.text
        send_data = {"networkInterface":networkInterface}

        t=Thread(target = self.sendData,args = (send_data,))
        t.daemon = True
        t.start()
        
    def go_Second(self):
        self.parent.get_screen('Second')


class SecondOneDataWindow(Screen):
    def go_SecondOne(self):
        self.parent.get_screen('SecondOne')


class SecondTwoWindow(Screen):
    def go_Second(self):
        self.parent.get_screen('Second')
        


class SecondThreeWindow(Screen):
    def go_Second(self):
        self.parent.get_screen('Second')





class WindowManager(ScreenManager):
    pass


class MyTestApp(App):
    NI = networkInterfaces
    def build(self):
        return Builder.load_file('exp.kv')


MyTestApp().run()