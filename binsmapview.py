from kivy.garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
from binmarker import BinMarker


def SelectBin(self, bin):
    lat, lon = bin[1], bin[2]
    marker = BinMarker(lat=lat, lon=lon, source="selected_marker.png")
    self.add_widget(marker)
    name = bin[0]
    self.bin_names.append(name)
    print('ok!!!')

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
        self.add_widget(marker)
        name = bin[0]
        self.bin_names.append(name)