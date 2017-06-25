from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, BooleanProperty
from kivy.config import Config
from pathlib import Path
from kivy.uix.widget import Widget
import os

import srs_connect, srs_crypt

#change checkbox place, next text filed when tabbed, delete verification mail
#begin at startup

class Login(Screen):
    current_state = None
    def login(self, username, password, mail_address, mail_pass):
        srs_connect.begin_login(username, password, mail_address, mail_pass)
        if self.current_state != self.ids.checkbox.state:
            if self.ids.checkbox.state == 'down': #It is checked
                file_open = open("srs_login.txt", "w")

                to_write = (self.ids.checkbox.state,
                            self.ids.username.text,
                            self.ids.password.text,
                            self.ids.mail_address.text,
                            self.ids.mail_pass.text
                            )

                for ele in to_write:
                    crypted = srs_crypt.encode(srs_crypt.key, ele)
                    file_open.write(crypted + "\n")

                file_open.close()
            else:
                my_file = Path(os.getcwd() + "/srs_login.txt")
                if my_file.is_file():
                    os.remove("srs_login.txt")
    def initialize(self):
        my_file = Path(os.getcwd() + "/srs_login.txt")
        if my_file.is_file():
            lines = []
            file_open = open("srs_login.txt")
            file_contents = file_open.readlines()
            for line in file_contents:
                lines.append(srs_crypt.decode(srs_crypt.key, line.rstrip("\n")))

            file_open.close()

            self.current_state = lines[0]
            self.ids.checkbox.state = lines[0]
            self.ids.username.text = lines[1]
            self.ids.password.text = lines[2]
            self.ids.mail_address.text = lines[3]
            self.ids.mail_pass.text = lines[4]

class LoginApp(App):
    Config.set('graphics', 'width', '325')
    Config.set('graphics', 'height', '525')
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()
        login_widget = Login(name='login')
        manager.add_widget(login_widget)
        login_widget.initialize()
        return manager

if __name__ == '__main__':
    LoginApp().run()
