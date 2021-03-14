import sqlite3
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from database import create_database, singup_test, insert_user, login_test, get_poits, insert_points, set_status, get_status, special_sing_up, special_login_test, insert_special_user, get_garbage_info, insert_new_garbage, garbage_taken
from kivymd.uix.button import MDRaisedButton
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window

create_database()

Window.size = (550, 800)

class LogInScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class SingUpScreen(Screen):
    pass

class InfoScreen(Screen):
    pass

class MenuScreen(Screen):
    pass


class PointsScreen(Screen):
    pass

class MenuScreenMain(Screen):
    pass

class SpecialLogInScreen(Screen):
    pass

class SpecialSingUpScreen(Screen):
    pass

class MapScreen1(Screen):
    pass

class MapScreen2(Screen):
    pass

class SpecialScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(LogInScreen(name='loginscreen'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(SingUpScreen(name='singupscreen'))
sm.add_widget(InfoScreen(name='infoscreen'))
sm.add_widget(MenuScreen(name='menuscreen'))
sm.add_widget(PointsScreen(name='points'))
sm.add_widget(MenuScreenMain(name='menuscreenmain'))
sm.add_widget(SpecialLogInScreen(name='specialloginscreen'))
sm.add_widget(SpecialSingUpScreen(name='specialsingupscreen'))
sm.add_widget(MapScreen1(name='MapScreen1'))
sm.add_widget(MapScreen2(name='MapScreen2'))
sm.add_widget(SpecialScreen(name = 'specialscreen'))

class MainApp(MDApp):
    def build(self):
        choises = ["Throw Away", "Main Page", "Points", "Log Out"]
        menu_items = [{"text": f"{i}"} for i in choises]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        self.menu.bind(on_release=self.menu_callback)

    def garbage_is_collected(self):
        user1 = self.get_special_user()
        garbage_taken(user1[0])
        insert_points(user1[0], 10)
        set_status('True')

    def bin_selected(self):
        insert_new_garbage(self.logged_in_user, self.kind_of_garbage)
        MDApp.get_running_app().root.current = 'menuscreenmain'
        set_status('True')
        self.state = 'Taken'

    def safe_kind_of_garbage(self, kind):
        self.kind_of_garbage = kind
        print(self.kind_of_garbage)

    def get_special_user(self):
        email = self.root.get_screen("specialloginscreen").ids.email_text1.text
        user = special_sing_up(email)
        return user

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, menu, item):

        self.menu.dismiss()
        #Snackbar(text=item.text).open()
        if item.text == 'Throw Away':
            MDApp.get_running_app().root.current = 'menuscreen'
        if item.text == 'Main Page':
            status = get_status()
            if status[0] == 'True':
                MDApp.get_running_app().root.current = 'menuscreenmain'
            else:
                MDApp.get_running_app().root.current = 'profile'
        if item.text == 'Points':
            user = self.get_user()
            points = get_poits(user[0])
            print(points)
            if points != None:
                self.root.get_screen('points').ids.info_label5.text = "Points: " + points[1]
            else:
                self.root.get_screen('points').ids.info_label5.text = "Points: 0"
            MDApp.get_running_app().root.current = 'points'
        if item.text == "Log Out":
            self.state = 'Taken'
            self.log_out()

    def see_points(self):
        user = self.get_user()
        points = get_poits(user[0])
        print(points)
        if points != None:
            self.root.get_screen('points').ids.info_label5.text = "Points: " + points[1]
        else:
            self.root.get_screen('points').ids.info_label5.text = "Points: 0"
        MDApp.get_running_app().root.current = 'points'

    def sing_up(self):
        username = self.root.get_screen("singupscreen").ids.username_text.text
        password = self.root.get_screen("singupscreen").ids.password_text.text
        email = self.root.get_screen("singupscreen").ids.email_text.text
        result = singup_test(email)

        if result == None and username != '' and password != '' and email != '':
            insert_user(username, email, password)
            set_status('False')
            self.reset_sing_up()
            MDApp.get_running_app().root.current = 'loginscreen'
        else:
            self.pop_up()

    def log_in(self):
        self.set_text_on_info()
        status = get_status()
        print(status[0])
        self.get_user()
        password = self.root.get_screen("loginscreen").ids.password_text.text
        email = self.root.get_screen("loginscreen").ids.email_text.text
        result = login_test(email, password)
        if result != None and password != '' and email != '':
            if status[0] == 'True':
                MDApp.get_running_app().root.current = 'menuscreenmain'
            else:
                MDApp.get_running_app().root.current = 'profile'
        else:
            self.pop_up()

    def special_login(self):
        password = self.root.get_screen("specialloginscreen").ids.password_text1.text
        email = self.root.get_screen("specialloginscreen").ids.email_text1.text
        result = special_login_test(email, password)
        if result != None and password != '' and email != '':
            MDApp.get_running_app().root.current = 'specialscreen'
        else:
            self.pop_up()

    def special_singup(self):
        username = self.root.get_screen("specialsingupscreen").ids.username_text.text
        password = self.root.get_screen("specialsingupscreen").ids.password_text.text
        email = self.root.get_screen("specialsingupscreen").ids.email_text.text
        result = special_sing_up(email)

        if result == None and username != '' and password != '' and email != '':
            insert_special_user(username, email, password)

            MDApp.get_running_app().root.current = 'specialloginscreen'
        else:
            self.pop_up()

    def get_user(self):
        email = self.root.get_screen("loginscreen").ids.email_text.text
        user = singup_test(email)
        self.logged_in_user = user[0]
        return user


    def set_text_on_info(self):
        self.kind_of_garbage = 'Plastic'
        user = self.get_user()
        status = get_garbage_info(user[0])
        kind = get_garbage_info(user[0])
        if status != None:
            self.root.get_screen('menuscreenmain').ids.info_label3.text = "Username: " + user[0] + "\nGarbage status: " + "Taken"
        else:
            self.root.get_screen('menuscreenmain').ids.info_label3.text = "Username: " + user[0] + "\nGarbage status: " + 'Not Taken'

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


MainApp().run()
