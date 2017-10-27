import requests
import json
import components.OsCommand as OsCommand

# The API URL is specific to your HUE bridge
HUE_API = "/api/kMLljmhPLjYjvqUwqAlI5AJWivt-FRyO06vT8my-"
DEBUG = False

class HueNotAvailableException(Exception):
    pass

class HueInterface(object):
    """
    This class provides a minimal Hue Interface.
    Check
    https://www.developers.meethue.com/documentation/getting-started
    To understand how to generate the proper Hue API interface connection
    """

    @property
    def api_url(self):
        """
        URL for HUE API. If the Hue bridge is not found this will raise an exception.
        :return: API URL
        """
        if self._api_url is None: raise HueNotAvailableException()
        return self._api_url

    def __init__(self):
        # Find HUE bridge on the network
        hue_ip = OsCommand.get_ip_for_hue_bridge()
        if hue_ip is None:
            print("Warning: HUE bridge not found.")
            self._api_url = None
        else:
            print("HUE bridge found on IP " + hue_ip)
            self._api_url = "http://" + hue_ip + HUE_API
            print("HUE API set to: " + self.api_url)

    def bridge_status(self):
        r = requests.get(self.api_url, timeout=5)
        if DEBUG: print(r.text)
        return r.text

    def turn_on(self, light_nbr):
        URL = self.api_url + "/lights/" + str(light_nbr) + "/state"
        data = {"on": True}  #, "sat": 254, "bri": 254, "hue": 5000}
        r = requests.put(URL, json.dumps(data), timeout=5)
        if DEBUG: print(r.text)
        return r.text

    def turn_off(self, light_nbr):
        URL = self.api_url + "/lights/" + str(light_nbr) + "/state"
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
        r = requests.get(self.api_url + "/lights/" + str(light_nbr), timeout=5)
        light_on = r.json()["state"]["on"]
        if light_on:
            self.turn_off(light_nbr)
            return False
        else:
            self.turn_on(light_nbr)
            return True

    def get_brightness(self, light_nbr):
        """
        Returns the current brightness of the light
        :param light_nbr: Number of the light from which to get the brightness.
        :return: Brightness
        """
        r = requests.get(self.api_url + "/lights/" + str(light_nbr), timeout=5)
        current_brightness = r.json()["state"]["bri"]
        return current_brightness

    def set_brightness(self, light_nbr, brightness):
        """
        Set the brightness of a light
        :param light_nbr: number of the light for which to set the brightness
        :param brightness: Brightness is a scale from 1 (the minimum the light is capable of) to 254 (the maximum).
               Note: a brightness of 1 is not off
        :return: None
        """""
        URL = self.api_url + "/lights/" + str(light_nbr) + "/state"
        data = {"on": True, "bri": brightness}
        r = requests.put(URL, json.dumps(data), timeout=5)
        if DEBUG: print(r.text)
        return r.text

    def set_brightness_up(self, light_nbr, amount=10):
        """
        Increases the brightness of a light
        :param light_nbr: number of the light for which to increase the brightness
        :param amount: increment to be used
        :return: None
        """""
        brightness = self.get_brightness(light_nbr) + amount
        if brightness > 254: brightness = 254
        self.set_brightness(light_nbr, brightness)

    def set_brightness_down(self, light_nbr, amount=10):
        """
        Decreases the brightness of a light
        :param light_nbr: number of the light for which to decrease the brightness
        :param amount: increment to be used
        :return: None
        """""
        brightness = self.get_brightness(light_nbr) - amount
        if brightness < 1: brightness = 1
        self.set_brightness(light_nbr, brightness)

    def set_color(self, light_nbr, hue, saturation):
        """
        Set the color of a light
        :param light_nbr: number of the light for which to set the color
        :param hue: The hue value is a wrapping value between 0 and 65535. Both 0 and 65535 are red, 25500 is green and 46920 is blue. 
        :param saturation: Saturation of the light. 254 is the most saturated (colored) and 0 is the least saturated (white).
        :return: None
        """""
        URL = self.api_url + "/lights/" + str(light_nbr) + "/state"
        data = {"on": True, "hue": hue, "sat": saturation}
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
    OsCommand.SCRIPTS_PATH = "./"
    Hue = HueInterface()
    # status = Hue.bridge_status()
    light_nbr = 2
    Hue.toggle(light_nbr)






