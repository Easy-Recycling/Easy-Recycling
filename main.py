from kivymd.app import MDApp
from kivy.app import App
from binsmapview import SelectBin
from binmarker import BinMarker
from binsmapview import BinsMapView
import sqlite3

#todo - suicide

class MainApp(MDApp):
    latitude = 42.69
    longitude = 23.34

    connection = None
    cursor = None
    def on_start(self):
        self.connection = sqlite3.connect("bins.db")
        self.cursor = self.connection.cursor()

    def bin_pos(self):
        bins_sum = []
        sum = 0
        app = App.get_running_app()
        sql_statement = "SELECT * FROM bins"
        app.cursor.execute(sql_statement)
        bins = app.cursor.fetchall()
        for bin in bins:
            sum = bin[1] + bin[2]
            bins_sum.append(sum)

        self.calculate_closest(bins_sum)

    def calculate_closest(self, bins_sum):
        loc_x, loc_y = 42.712630, 23.259306
        min = 0
        location_sum = loc_x + loc_y
        for i in range (0, 6):
            distance = location_sum - bins_sum[i]
            if distance < 0:
                distance *= -1

            if i == 1:
                min = distance
                closest_bin = i

            if distance < min:
                min = distance
                closest_bin = i
        app = App.get_running_app()
        sql_statement = "SELECT * FROM bins"
        app.cursor.execute(sql_statement)
        bins = app.cursor.fetchall()
        i = 1
        for bin in bins:
            i+=1
            if i == closest_bin:
                self.SelectBin(bin)


    def build(self):
        return


MainApp().run()
