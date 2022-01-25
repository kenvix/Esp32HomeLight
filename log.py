import sys
import time

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def print_log(level, message):
    t = time.time()
    # if int(t) < 696432783:
    #     t = str(t)
    # else:
    #     t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    eprint("[%s][%s] %s" % (t, level, str(message)))

def trace(message):
    print_log("Trace", message)

def debug(message):
    print_log("Debug", message)

def info(message):
    print_log("Info", message)

def warn(message):
    print_log("Warn", message)

def error(message):
    print_log("Error", message)

def severe(message):
    print_log("Severe", message)

if __name__ == "__main__":
    info("test")