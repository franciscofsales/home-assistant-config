import appdaemon.plugins.hass.hassapi as hass
import datetime

class AutoAdjust(hass.Hass):
    def initialize(self):
        # Add api endpoints for REST https://appdaemon.readthedocs.io/en/latest/APPGUIDE.html?#restful-api-support
        self.register_endpoint(self.adjust_night, "adjust_night")
        self.register_endpoint(self.adjust_morning, "adjust_morning")

        # Compute our times
        self.morning_adjust_weekday = datetime.datetime.strptime(self.args["morning_adjust_weekday"], '%H:%M:%S').time()
        self.night_adjust_weekday = datetime.datetime.strptime(self.args["night_adjust_weekday"], '%H:%M:%S').time()
        self.morning_adjust_weekend = datetime.datetime.strptime(self.args["morning_adjust_weekend"], '%H:%M:%S').time()
        self.night_adjust_weekend = datetime.datetime.strptime(self.args["night_adjust_weekend"], '%H:%M:%S').time()

        # Set our time callbacks
        self.run_daily(self.adjust_morning, self.morning_adjust_weekday, constrain_days="mon,tue,wed,thu,fri")
        self.run_daily(self.adjust_night, self.night_adjust_weekday, constrain_days="mon,tue,wed,thu,fri")
        self.run_daily(self.adjust_morning, self.morning_adjust_weekend, constrain_days="sat,sun")
        self.run_daily(self.adjust_night, self.night_adjust_weekend, constrain_days="sat,sun")

        # Set our device tracker callbacks
        if "device_tracker" in self.args:
            for device in self.split_device_list(self.args["device_tracker"]):
                self.listen_state(self.presence_adjust, device)

        # Set our door trigger callback
        self.listen_state(self.presence_adjust, self.args["door_trigger"])

    # Determine whether we're in daytime or nighttime
    def time_in_range(self, start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    # Function to adjust temperature(s)
    def adjust_temp(self, kwargs):
        for tstat in self.split_device_list(self.args["thermostats"]):
            self.call_service("climate/set_temperature", entity_id = tstat, temperature = kwargs["temp"])

    # Change temperature in response to device tracker or door sensor
    def presence_adjust(self, entity, attribute, old, new, kwargs):
        # Do nothing if AC off
        if self.get_state("sensor.thermostat_operating_mode").lower == "off":
            return

        # If tracker changes to "home" OR the front door opens when no one was home
        if (old == "not_home" and new == "home") or (old == "off" and new == "on" and self.get_state(self.args["device_tracker"]) == "not_home"):
            if old == "off" and new == "on":
                self.log("Door open detected: {}".format(entity))
                #self.set_state(self.args["device_tracker"], state = "home")

            # Someone is home (door or tracker) decide if it's night or day and adjust accordingly
            if self.time_in_range(self.morning_adjust_weekday, self.night_adjust_weekday, datetime.datetime.now().time()) == True:
                self.log("Someone came home during the day: {}".format(entity))
                self.adjust_morning(kwargs)
            else:
                self.log("Someone came home at night: {}".format(entity))
                self.adjust_night(kwargs)

        # If someone was home but the house is now unoccupied
        elif old == "home" and new == "not_home":
            self.log(self.get_state("sensor.thermostat_operating_mode").lower())
            if self.get_state("sensor.thermostat_operating_mode").lower() == "heat":
                self.log("Mode: Heat Unoccupied -- %s" % self.args["heat_unoccupied"])
                self.run_in(self.adjust_temp, 5, temp = self.args["heat_unoccupied"])

            elif self.get_state("sensor.thermostat_operating_mode").lower() == "cool":
                self.log("Mode: Cool Unoccupied -- %s" % self.args["cool_unoccupied"])
                self.run_in(self.adjust_temp, 5, temp = self.args["cool_unoccupied"])

    # Set day time temperature
    def adjust_morning(self, *kwargs):
        if self.get_state(self.args["device_tracker"]) == "home":
            # Do nothing if AC off
            if self.get_state("sensor.thermostat_operating_mode").lower() == "off":
                return

            elif self.get_state("sensor.thermostat_operating_mode").lower() == "heat":
                self.log("Mode: Heat Day -- %s" % self.args["heat_day"])
                self.run_in(self.adjust_temp, 1, temp = self.args["heat_day"])

            elif self.get_state("sensor.thermostat_operating_mode").lower() == "cool":
                self.log("Mode: Cool Day -- %s" % self.args["cool_day"])
                for tstat in self.split_device_list(self.args["thermostats"]):
                    self.run_in(self.adjust_temp, 1, temp = self.args["cool_day"])

        # No one is home and we've gotten called to adjust for day based on time
        else:
            # Do nothing if AC off
            if self.get_state("sensor.thermostat_operating_mode").lower() == "off":
                return

            if self.get_state("sensor.thermostat_operating_mode").lower() == "heat":
                self.log("Mode: Heat Unoccupied -- %s" % self.args["heat_unoccupied"])
                self.run_in(self.adjust_temp, 1, temp = self.args["heat_unoccupied"])

            elif self.get_state("sensor.thermostat_operating_mode").lower() == "cool":
                self.log("Mode: Cool Unoccupied -- %s" % self.args["cool_unoccupied"])
                self.run_in(self.adjust_temp, 1, temp = self.args["cool_unoccupied"])

        # For appdaemon api: curl -i -X POST -H "Content-Type: application/json" http://10.0.1.22:8888/api/appdaemon/adjust_morning
        response = ""
        return response, 200


    def adjust_night(self, *kwargs):
        if self.get_state(self.args["device_tracker"]) == "home":
            # Do nothing if AC off
            if self.get_state("sensor.thermostat_operating_mode").lower() == "off":
                return

            if self.get_state("sensor.thermostat_operating_mode").lower() == "heat":
                self.log("Mode: Heat Night -- %s" % self.args["heat_night"])
                self.run_in(self.adjust_temp, 1, temp = self.args["heat_night"])

            elif self.get_state("sensor.thermostat_operating_mode").lower() == "cool":
                self.log("Mode: Cool Night -- %s" % self.args["cool_night"])
                self.run_in(self.adjust_temp, 1, temp = self.args["cool_night"])

        # No one is home and we've gotten called back to adjust for night based on time
        else:
            # Do nothing if AC off
            if self.get_state("sensor.thermostat_operating_mode").lower() == "off":
                return

            if self.get_state("sensor.thermostat_operating_mode").lower() == "heat":
                self.log("Mode: Heat Unoccupied -- %s" % self.args["heat_unoccupied"])
                self.run_in(self.adjust_temp, 1, temp = self.args["heat_unoccupied"])

            elif self.get_state("sensor.thermostat_operating_mode").lower() == "cool":
                self.log("Mode: Cool Unoccupied -- %s" % self.args["cool_unoccupied"])
                self.run_in(self.adjust_temp, 1, temp = self.args["cool_unoccupied"])

        # For appdaemon api: curl -i -X POST -H "Content-Type: application/json" http://10.0.1.22:8888/api/appdaemon/adjust_night
        response = ""
        return response, 200
