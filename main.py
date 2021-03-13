from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivy.garden.mapview import MapView
from kivy.clock import Clock
from binmarker import BinMarker
import sqlite3


class BinsMapView(MapView):
    getting_bins_timer = None
    bin_names = []

    def start_getting_bins_in_fov(self):
        try:
            self.getting_bins_timer.cancel()
        except:
            pass

        self.getting_bins_timer = Clock.schedule_once(self.get_bins_in_fov, 1)

    def get_bins_in_fov(self, *args):
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()
        app = App.get_running_app()
        sql_statement = "SELECT * FROM bins WHERE location_x > %s AND location_x < %s AND location_y > %s AND location_y < %s "%(min_lat, max_lat, min_lon, max_lon)
        app.cursor.execute(sql_statement)
        bins = app.cursor.fetchall()
        print(bins)
        for bin in bins:
            name = bin[0]
            if name in self.bin_names:
                continue
            else:
                self.add_bin(bin)

    def add_bin(self, bin):
        lat, lon = bin[1], bin[2]
        marker = BinMarker(lat=lat, lon=lon, source="marker.png")
        marker.add_widget(Button(size_hint=(1, .4), text=('Select Bin'), on_release=(self.proceed)))
        self.add_widget(marker)
        name = bin[0]
        self.bin_names.append(name)

    def proceed(self, *args):
        print("proceed")


class MainApp(MDApp, MapView):
    latitude = 42.69
    longitude = 23.34
    selected_name = []

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
        global closest_bin
        loc_x, loc_y = 42.712630, 23.259306
        min = 0
        location_sum = loc_x + loc_y
        for i in range (0, 6):
            distance = location_sum - bins_sum[i]
            if distance < 0:
                distance *= -1

            if i == 0:
                min = distance
                closest_bin = i

            if distance < min:
                min = distance
                closest_bin = i

        app = App.get_running_app()
        sql_statement = "SELECT * FROM bins"
        app.cursor.execute(sql_statement)
        bins = app.cursor.fetchall()
        i = 0
        for bin in bins:
            if i == closest_bin:
                self.root.center_on(bin[1], bin[2])
                self.root.zoom = 17

            i += 1


    def build(self):
        return


MainApp().run()
