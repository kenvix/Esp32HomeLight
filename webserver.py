from MicroWebSrv2 import *
import time

server = MicroWebSrv2()

def start():
    server.BindAddress = ('0.0.0.0', 12345)
    server.RootPath = 'www'
    server.StartManaged(parllProcCount=3)


if __name__ == "__main__":
    start()
    try :
        while True :
            sleep(1)
    except KeyboardInterrupt :
        server.Stop()