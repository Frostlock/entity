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

    def bridge_status(self):
        r = requests.get(HUE_BRIDGE_URL, timeout=5)
        print(r.content)

    def turn_on(self,light_nbr):
        URL = HUE_BRIDGE_URL + "/lights/" + str(light_nbr) + "/state"
        data = {"on": True, "sat": 254, "bri": 254, "hue": 5000}
        r = requests.put(URL, json.dumps(data), timeout=5)
        print(r.content)

    def turn_off(self, light_nbr):
        URL = HUE_BRIDGE_URL + "/lights/" + str(light_nbr) + "/state"
        data = {"on": False}
        r = requests.put(URL, json.dumps(data), timeout=5)
        print(r.content)


if __name__ == '__main__':
    DEBUG = True
    Hue = HueInterface()

    # Get all Hue information from the API
    Hue.bridge_status()


