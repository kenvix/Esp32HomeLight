from config import netconfig
import _thread
import picoweb

app = picoweb.WebApp(netconfig.DEVICE_NAME)

def _start(port=80):
    app.run("0.0.0.0", port)
    pass

def start(port=80):
    _thread.start_new_thread(_start, ((port,)))