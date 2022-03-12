import appdaemon.plugins.hass.hassapi as hass
from core.math import MovingAverage

#
# Average Power Consumption Manager
#
# Args: 
#   sensor: Power sensor
#   ticks: Queue length in Tibber ticks (1 tick = 2 seconds)
#   wait: Wait time in seconds for scheduler updating HASS
#   input_field: HASS input field to update
#

class AveragePowerConsumption(hass.Hass):
    def initialize(self):
        
        sensor = self.args['sensor']  # 1 Tibber tick = 2 sec 
        ticks = self.args['ticks']  # 1 Tibber tick = 2 sec
        wait = self.args['wait']  # Wait time in seconds for scheduler
        self.input_field = self.args['input_field']  # HASS input field to update

        self.moving_average = MovingAverage(ticks)

        self.listen_state(self.sensor_change_cb, sensor)
        self.run_every(self.update_hass_sched, f'now+{wait}', wait)  # Wait 10 onstart and update every wait sec

    def sensor_change_cb(self, entity, attribute, old, new, kwargs):
        self.average = self.moving_average.next(float(new))

    def update_hass_sched(self, kwargs):
        power = round(self.average, 0)
        self.log(f'HASS:{self.input_field}={power}')
        return self.set_value(self.input_field, power)
