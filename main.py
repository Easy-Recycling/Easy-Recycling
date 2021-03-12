import sqlite3
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from database import create_database, singup_test, insert_user, login_test
from kivymd.uix.button import MDRaisedButton
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog

conn = sqlite3.connect('UsersTry.db')
c = conn.cursor()
create_database()

#Window.size = (1040, 1426)

class LogInScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass

class SingUpScreen(Screen):
    pass

class InfoScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(LogInScreen(name='loginscreen'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(SingUpScreen(name='singupscreen'))
sm.add_widget(InfoScreen(name='infoscreen'))



class AllHere(MDApp):
    screen_manager = ObjectProperty()  # IMPORTANT!

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def build(self):
        kinds_of_bins = ["Metal", "Rubber", "Plastic"]
        menu_items = [{"text": f"{i}"} for i in kinds_of_bins]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        self.menu.bind(on_release=self.menu_callback)


    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, menu, item):
        self.menu.dismiss()
        Snackbar(text=item.text).open()


    def sing_up(self):
        username = self.root.get_screen("singupscreen").ids.username_text.text
        password = self.root.get_screen("singupscreen").ids.password_text.text
        email = self.root.get_screen("singupscreen").ids.email_text.text
        result = singup_test(email)

        if result == None and username != '' and password != '' and email != '':
            insert_user(username, email, password)
            conn.commit()
            self.reset_sing_up()
            MDApp.get_running_app().root.current = 'loginscreen'
        else:
            self.pop_up()

    def log_in(self):
        self.set_text_on_info()
        password = self.root.get_screen("loginscreen").ids.password_text.text
        email = self.root.get_screen("loginscreen").ids.email_text.text
        result = login_test(email, password)
        if result != None and password != '' and email != '':
            #self.reset_log_in()
            self.get_user()
            MDApp.get_running_app().root.current = 'profile'
        else:
            self.pop_up()

    def get_user(self):
        email = self.root.get_screen("loginscreen").ids.email_text.text
        user = singup_test(email)
        return user

    def get_rubbish_kind(self):
        pass

    def set_text_on_info(self):
        user = self.get_user()
        length = len(user[0])
        kind_of_rubbish = 'rubber'
        self.root.get_screen('infoscreen').ids.info_label.text = "Username: " + user[0] + "\nok"

    def log_out(self):
        self.reset_log_in()
        MDApp.get_running_app().root.current = 'loginscreen'

    def pop_up(self):
        dialog = MDDialog(text="Incorrect login/sing up information, try again")
        dialog.open()

    #def set_screen(self):
        #MDApp.get_running_app().root.current = 'profile'

    def reset_sing_up(self):
        self.root.get_screen("singupscreen").ids.username_text.text = ''
        self.root.get_screen("singupscreen").ids.password_text.text = ''
        self.root.get_screen("singupscreen").ids.email_text.text = ''

    def reset_log_in(self):
        self.root.get_screen("loginscreen").ids.password_text.text = ''
        self.root.get_screen("loginscreen").ids.email_text.text = ''

    def createButton(self):
        print("button created")
        x = 0.5
        y = 0.6

        btn = MDRaisedButton(text="New Button", pos_hint={'center_x': x, 'center_y': y})
        self.root.ids.screenID.add_widget(btn)

    #def new_window(self, *args):
     #   btn = MDFlatButton(text="New group", size_hint_y=None, height=100)
      #  self.root.add_widget(btn)


AllHere().run()
