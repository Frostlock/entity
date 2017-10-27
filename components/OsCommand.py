from subprocess import Popen, run, PIPE, TimeoutExpired
from time import sleep

SCRIPTS_PATH = "./components/"

def get_ip_for_mac(mac):
    """
    Calls a shell script to retrieve the IP for the given Mac address.
    The underlying shell script uses the arp table to figure out the IP.
    :param mac: mac address for which you want to retrieve the IP
    :return: IP
    """
    result = run([SCRIPTS_PATH + "OsCommand-GetIpForMac.sh", mac], stdout=PIPE)
    result.check_returncode()
    lines = result.stdout.decode('utf-8').splitlines()
    if len(lines) > 0:
        return lines[0]
    else:
        return None

def get_ip_for_hue_bridge():
    """
    Calls a shell script to retrieve the IP for the HUE bridge.
    :return: IP or None
    """
    result = run([SCRIPTS_PATH + "OsCommand-GetIpForHueBridge.sh"], stdout=PIPE)
    result.check_returncode()
    lines = result.stdout.decode('utf-8').splitlines()
    if len(lines) > 0:
        return lines[0]
    else:
        return None

def system_reboot():
    """
    Reboots the entire system.
    :return: None
    """
    sleep(5)
    run([SCRIPTS_PATH + "OsCommand-SystemReboot.sh"])

def system_shutdown():
    """
    Shuts down the entire system.
    :return: None
    """
    sleep(5)
    run([SCRIPTS_PATH + "OsCommand-SystemShutdown.sh"])

if __name__ == '__main__':
    SCRIPTS_PATH = "./"

    #print(get_ip_for_hue_bridge())

    # p = ping_sweep()
    # while p.poll() is None:
    #     print("Waiting on ping sweep")
    #     try:
    #         p.wait(timeout=5)
    #     except TimeoutExpired:
    #         pass

    print(get_ip_for_mac("00:17:88:71:33:87"))