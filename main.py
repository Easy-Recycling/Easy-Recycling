import sqlite3
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from database import create_database, singup_test, insert_user, login_test
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.lang import Builder

conn = sqlite3.connect('UsersTry.db')
c = conn.cursor()
create_database()


class LogInScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


class SingUpScreen(Screen):
    pass



sm = ScreenManager()
sm.add_widget(LogInScreen(name='loginscreen'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(SingUpScreen(name='singupscreen'))


class AllHere(MDApp):

    def sing_up(self):
        username = self.root.get_screen("singupscreen").ids.username_text.text
        password = self.root.get_screen("singupscreen").ids.password_text.text
        email = self.root.get_screen("singupscreen").ids.email_text.text
        result = singup_test(email)

        if result == None and username != '' and password != '' and email != '':
            insert_user(username, password, email)
            conn.commit()
            self.reset_sing_up()
            MDApp.get_running_app().root.current = 'loginscreen'
        else:
            self.pop_up()

    def log_in(self):
        self.set_text()
        password = self.root.get_screen("loginscreen").ids.password_text.text
        email = self.root.get_screen("loginscreen").ids.email_text.text
        result = login_test(email, password)
        if result != None and password != '' and email != '':
            self.reset_log_in()
            MDApp.get_running_app().root.current = 'profile'
        else:
            self.pop_up()

    def set_text(self):
        self.root.get_screen('profile').ids.button_test.text = 'kolio'
        pass

    def pop_up(self):
        dialog = MDDialog(text="Incorrect login/sing up information, try again")
        dialog.open()

    # def set_screen(self):
    # MDApp.get_running_app().root.current = 'profile'

    def reset_sing_up(self):
        self.root.get_screen("singupscreen").ids.username_text.text = ''
        self.root.get_screen("singupscreen").ids.password_text.text = ''
        self.root.get_screen("singupscreen").ids.email_text.text = ''

    def reset_log_in(self):
        self.root.get_screen("loginscreen").ids.password_text.text = ''
        self.root.get_screen("loginscreen").ids.email_text.text = ''

    def on_start(self):
        # Create dropdown menu
        self.dropdown = MDDropdownMenu(width_mult=4)

        # Add items to the menu
        for i in range(4):
            self.dropdown.items.append(
                {"viewclass": "MDMenuItem",
                 "text": "Map" + str(i),
                 "callback": self.map_callback}
            )

    def map_callback(self, text_of_the_option):
        print(text_of_the_option)


AllHere().run()