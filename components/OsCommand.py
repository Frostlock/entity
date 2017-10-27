from subprocess import Popen, run, PIPE, TimeoutExpired

SCRIPTS_PATH = "./components/"

def ping_sweep():
    """
    Triggers a ping sweep which will populate the arp table.
    The call will return immediately and the ping sweep will run in the background.
    :return: Popen object to interact with the ping sweep process
    """
    return Popen([SCRIPTS_PATH + "OsCommand-PingSweep.sh"])

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

if __name__ == '__main__':
    SCRIPTS_PATH = "./"
    p = ping_sweep()
    while p.poll() is None:
        print("Waiting on ping sweep")
        try:
            p.wait(timeout=5)
        except TimeoutExpired:
            pass
    #print(get_ip_for_mac("00:17:88:71:33:87"))