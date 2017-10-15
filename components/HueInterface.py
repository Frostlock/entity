import requests
import json

HUE_BRIDGE_URL = "http://192.168.0.115/api/kMLljmhPLjYjvqUwqAlI5AJWivt-FRyO06vT8my-"
DEBUG = False

class HueInterface(object):
    """
    This class provides a minimal Hue Interface.
    Check
    https://www.developers.meethue.com/documentation/getting-started
    To understand how to generate the proper Hue API interface connection
    """

    def __init__(self):
        pass
        #TODO: read config (nbr of lights etc...)

    def bridge_status(self):
        r = requests.get(HUE_BRIDGE_URL, timeout=5)
        if DEBUG: print(r.text)
        return r.text

    def turn_on(self,light_nbr):
        URL = HUE_BRIDGE_URL + "/lights/" + str(light_nbr) + "/state"
        data = {"on": True}  #, "sat": 254, "bri": 254, "hue": 5000}
        r = requests.put(URL, json.dumps(data), timeout=5)
        if DEBUG: print(r.text)
        return r.text

    def turn_off(self, light_nbr):
        URL = HUE_BRIDGE_URL + "/lights/" + str(light_nbr) + "/state"
        data = {"on": False}
        r = requests.put(URL, json.dumps(data), timeout=5)
        if DEBUG: print(r.text)
        return r.text

    def toggle(self, light_nbr):
        """
        Toggle light on or off
        :param light_nbr: number of the light to be toggled
        :return: Boolean status of light (True=On, False=Off)
        """
        r = requests.get(HUE_BRIDGE_URL + "/lights/" + str(light_nbr), timeout=5)
        light_on = r.json()["state"]["on"]
        if light_on:
            self.turn_off(light_nbr)
            return True
        else:
            self.turn_on(light_nbr)
            return False

if __name__ == '__main__':
    DEBUG = True
    Hue = HueInterface()
    # status = Hue.bridge_status()
    light_nbr = 2
    Hue.toggle(light_nbr)






