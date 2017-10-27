from subprocess import run, PIPE

def get_ip_for_mac(mac):
    """
    Calls a shell script to retrieve the IP for the given Mac address.
    The underlying shell script uses the arp table to figure out the IP.
    :param mac: mac address for which you want to retrieve the IP
    :return: IP
    """
    result = run(["./components/OsCommand-GetIpForMac.sh", mac], stdout=PIPE)
    result.check_returncode()
    lines = result.stdout.decode('utf-8').splitlines()
    if len(lines) > 0:
        return lines[0]
    else:
        return None