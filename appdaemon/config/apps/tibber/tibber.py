import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime
from manager import TibberPriceManager

#
# Average Power Consumption Manager
#
# Args: 
#
#

class PriceManager(hass.Hass):
    
    def initialize(self):
        self.price_manager = TibberPriceManager()  # Get Tibber prices Manager
        runtime = datetime.now().replace(minute=0, second=0, microsecond=0)
        self.run_hourly(self.run_hourly_callback, runtime)  # Update HASS every hour
        self.update_power_level()  # Update HASS now

    def update_power_level(self):
        price = self.price_manager.updater()
        self.log(price.level)
        self.select_option("input_select.power_level", price.level)

    def run_hourly_callback(self, kwargs):
        self.update_power_level()
