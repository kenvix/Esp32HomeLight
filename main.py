import os
import sys 
import log
import network
import config
import time
import install
from network import WLAN
from lib import utelnetserver
from lib import ftp_thread

sta_if: WLAN = None
ap_if: WLAN = None


def setupAP():
    log.info("Setting up AP with SSID %s     Key %s" % (config.DEVICE_NAME, config.AP_WPA_KEY))
    global ap_if
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid=config.DEVICE_NAME, password=config.AP_WPA_KEY)
    if len(config.AP_WPA_KEY) > 8:
        ap_if.config(authmode = network.AUTH_WPA_WPA2_PSK)
    else:
        log.warn("No AP password set or password is too short")

    # No network, not a gateway
    ap_if.ifconfig((config.AP_IP, '255.255.255.0', config.AP_GATEWAY, config.AP_DNS))
    log.info("AP Config: %s" % str(ap_if.ifconfig()))


def waitAPUp():
    global ap_if
    while ap_if.active() == False:
        time.sleep(0.3)
        pass
    log.info("AP %s is up" % config.DEVICE_NAME)


def setupFTP():
    log.info("Starting FTP")
    try:
        import _thread
        _thread.start_new_thread(ftp_thread.ftpserver, ((True,)))
    except:
        ftp_thread.ftpserver(False)



def setupSTA():
    global sta_if 
    if len(config.STA_SSID) < 1:
        log.info("STA not configured, skip")
    else:
        log.info("Setting up STA with SSID %s     Key %s" % (config.STA_SSID, config.STA_WPA_KEY))
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active()
        sta_if.connect(config.STA_SSID, config.STA_WPA_KEY)


def waitSTAUp():
    global sta_if 
    while sta_if.isconnected() == False:
        time.sleep(0.3)
        pass
    log.info("STA %s is up" % config.STA_SSID)
    log.info("STA Connection info: %s" % str(sta_if.ifconfig()))


def main():
    log.info("Kenvix Home Light Controller v1.0")
    log.info("System info: %s" % str(os.uname()))

    try:
        setupAP()
        waitAPUp()
    except Exception as e:
        log.error("Setup Wi-FI AP FAILED!")
        sys.print_exception(e, sys.stderr)

    try:
        setupFTP()
    except Exception as e:
        log.error("Setup FTP server FAILED!")
        sys.print_exception(e, sys.stderr)

    pass

if __name__ == "__main__":
    main()