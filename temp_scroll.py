from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty, ReferenceListProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import psutil
from threading import Thread
import functools
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.properties import StringProperty
import requests
from kivy.config import Config
from kivymd.app import MDApp
Config.set('graphics', 'resizable', True)
import whois
import socket
import json




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
    state = StringProperty("stop")
    def on_state(self, instance, value):
        {
        "start": self.ids.progress.start,
        "stop": self.ids.progress.stop,
        }.get(value)()


class SecondTwoWindow(Screen):
    temp = 'Enter Domain in the text Field'
    def go_Second(self):
        self.parent.get_screen('Second')
    
    def ip_to_loc_write(self):
        self.temp = self.ids.ip_to_loc.text
    
    def get_Host_name_IP(self, host_name): 
        try: 
            host_ip = socket.gethostbyname(host_name) 
            return host_ip
            # print("Hostname : ",host_name) 
            # print("IP : ",host_ip) 
        except: 
            return "Unable to get Hostname and IP"
    def get_location(self,ip):
        ip_address = ip
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result  = json.loads(result)
        return result
    
    def ip_to_loc_press(self):
        ip_addr = self.get_Host_name_IP(self.temp)
        loc = self.get_location(ip_addr)
        self.ids.ip_to_loc_show.text =  "IP Address : " + str(loc.get('IPv4')) + "\n" + "Country Code : " + str(loc.get('country_code')) \
                                        +"\n" + "Country : " + str(loc.get('country_name')) +"\n" + "city : " + str(loc.get('city')) \
                                        +"\n" + "Postal Code : " + str(loc.get('postal')) +"\n" + "Latitude : " + str(loc.get('latitude')) \
                                        +"\n" + "Longitude : " + str(loc.get('longitude')) +"\n" + "State : " + str(loc.get('state'))
                                        

global tem
tem = ''
class SecondThreeWindow(Screen):
    # temp = 'Enter Domain in the Text Field'
    def go_Second(self):
        self.parent.get_screen('Second')
        
        
    def whois_press(self):
        self.tem = self.ids.input_whois.text 
        
    def whois_button(self):
        self.parent.get_screen('SecondThreeData')

class SecondThreeDataWindow(Screen):
    def build(self):
        w = whois.whois(tem)
        self.ids.show_whois_text.text = str(w)
    
    def go_Second_three(self):
        self.parent.get_screen('SecondThree')
    

class WindowManager(ScreenManager):
    pass


class MyTestApp(MDApp):
    NI = networkInterfaces
    def build(self):
        return Builder.load_file('exp.kv')


MyTestApp().run()