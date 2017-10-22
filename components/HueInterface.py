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

    def turn_on(self, light_nbr):
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
            return False
        else:
            self.turn_on(light_nbr)
            return True

    def set_color(self, light_nbr, hue, saturation):
        """
        Set the color of a light
        :param light_nbr: number of the light for which to set the color
        :param hue: The hue value is a wrapping value between 0 and 65535. Both 0 and 65535 are red, 25500 is green and 46920 is blue. 
        :param saturation: Saturation of the light. 254 is the most saturated (colored) and 0 is the least saturated (white).
        :return: None
        """""
        URL = HUE_BRIDGE_URL + "/lights/" + str(light_nbr) + "/state"
        data = {"on": True, "hue": hue, "sat": saturation, "bri": 254}
        print(data)
        r = requests.put(URL, json.dumps(data), timeout=5)
        if DEBUG: print(r.text)
        return r.text

    def set_pygame_color(self, light_nbr, pygame_color):
        """
        Set the color of a light based on a pygame color.
        This method will handle the conversion of pygame HSV space to Philips HSV space.
        :param light_nbr: number of the light for which to set the color
        :param pygame_color: a pygame color object
        :return: None
        """
        assert type(pygame_color).__name__ == "Color"
        # Get pygame color Hue and Saturation values
        h = pygame_color.hsva[0]
        s = pygame_color.hsva[1]
        # Convert to Philips HUE range hue and saturation
        # Pygame hue is in [0, 360] and saturation in [0, 100]
        # Philips HUE hue is in[0, 65535] and saturation in [0, 254].
        h = int((h / 360) * 65535)
        s = int((s / 100) * 254)
        # Set color of light
        self.set_color(light_nbr, h, s)


if __name__ == '__main__':
    DEBUG = True
    Hue = HueInterface()
    # status = Hue.bridge_status()
    light_nbr = 2
    Hue.toggle(light_nbr)






