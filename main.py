import os
import sys
import log
import network
from config import netconfig
import time
import install
from network import WLAN
from lib import utelnetserver
from lib import ftp_thread
import uos
import ntptime
from machine import Timer

sta_if: WLAN = None
ap_if: WLAN = None

ntp_timer: Timer = None

def setupAP():
    log.info("Setting up AP with SSID %s     Key %s" % (netconfig.DEVICE_NAME, netconfig.AP_WPA_KEY))
    global ap_if
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid=netconfig.DEVICE_NAME, password=netconfig.AP_WPA_KEY)
    if len(netconfig.AP_WPA_KEY) > 8:
        ap_if.config(authmode = network.AUTH_WPA_WPA2_PSK)
    else:
        log.warn("No AP password set or password is too short")

    # No network, not a gateway
    ap_if.ifconfig((netconfig.AP_IP, '255.255.255.0', netconfig.AP_GATEWAY, netconfig.AP_DNS))
    log.info("AP Config: %s" % str(ap_if.ifconfig()))


def waitAPUp():
    global ap_if
    while ap_if.active() == False:
        time.sleep(0.3)
        pass
    log.info("AP %s is up" % netconfig.DEVICE_NAME)


def setupFTP():
    log.info("Starting FTP")
    try:
        import _thread
        _thread.start_new_thread(ftp_thread.ftpserver, ((True,)))
    except:
        ftp_thread.ftpserver(False)



def setupSTA():
    global sta_if 
    if len(netconfig.STA_SSID) < 1:
        log.info("STA not configured, skip")
    else:
        log.info("Setting up STA with SSID %s     Key %s" % (netconfig.STA_SSID, netconfig.STA_WPA_KEY))
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active()
        sta_if.connect(netconfig.STA_SSID, netconfig.STA_WPA_KEY)


def waitSTAUp():
    global sta_if 
    if sta_if is not None:
        while sta_if.isconnected() == False:
            time.sleep(0.3)
            pass
        log.info("STA %s is up" % netconfig.STA_SSID)
        log.info("STA Connection info: %s" % str(sta_if.ifconfig()))


def setupNTP():
    global sta_if, ntp_timer
    if sta_if is None:
        log.info("STA not configured, skip NTP client") 
    else:
        try:
            ntptime.NTP_DELTA = netconfig.TIMEZONE_DELTA   # 可选 UTC+8偏移时间（秒），不设置就是UTC0
            ntptime.host = netconfig.NTP_HOST  # 可选，ntp服务器，默认是"pool.ntp.org"
            ntptime.settime()   # 修改设备时间,到这就已经设置好了
            log.info("NTP time synced. Sync again after 6h")
            ntp_timer = Timer(period=6 * 60 * 60 * 1000, mode=Timer.ONE_SHOT, callback=setupNTP)
        except Exception as e:
            log.error("NTP time Sync failed, retry after 3s")
            sys.print_exception(e, sys.stderr)
            ntp_timer = Timer(period=3000, mode=Timer.ONE_SHOT, callback=setupNTP)
        pass


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

    try:
        setupSTA()
        waitSTAUp()
    except Exception as e:
        log.error("Setup Wi-FI STA FAILED!")
        sys.print_exception(e, sys.stderr)

    setupNTP()
    pass

if __name__ == "__main__":
    main()