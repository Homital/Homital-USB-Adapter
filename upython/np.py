from machine import Pin
import homital
import time

USBOUT = Pin(0, Pin.OUT)

def startup():
    pass

def showerror():
    time.sleep(2)

def connecting():
        time.sleep(5)

def default_mode(update_interval_ms):
    print("Running np.default_mode(%d)" % (update_interval_ms,))
    while True:
        try:
            st = homital.getStatus()
            print('status: %s' % (str(st),))
            if st['success']:
                st = st['status']
                power = st['power']
                if power:
                    USBOUT.on()
                else:
                    USBOUT.off()
            else:
                print('getting status failed')
        except:
            print("unknown error when getting status")
        time.sleep_ms(update_interval_ms)

def main():
    print('Running np.main()')
    print('Testing connection to Homital-Core...')
    connecting()
    if (not homital.isConnected()):
        print('Connection Failed!')
        while True:
            showerror()
    print('Connected!')
    try:
        import modes
    except:
        default_mode(1000)