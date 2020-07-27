#import wifimgr
import network
from time import sleep
import db
import readcmd
import np

np.startup()

# Connect to Wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
while not wlan.isconnected():
    print("connecting to wifi...")
    try:
        wifissid = db.read(b'wifissid').decode('utf-8')
        wifipswd = db.read(b'wifipassword').decode('utf-8')
        if wifissid == '-1' or wifipswd == '-1':
            raise Exception('Wifi Credentials not set')
        wlan.connect(wifissid, wifipswd)
        for i in range(3): # 3 rounds
            np.connecting()
    except:
        print("Error connecting to wifi")
        np.showerror()
        while readcmd.readcmd():
            pass
print('network config:', wlan.ifconfig())

# Connect to Homital-Core
while True:
    deviceName = db.read(b'deviceName').decode('utf-8')
    roomId = db.read(b'roomId').decode('utf-8')
    roomUser = db.read(b'roomUser').decode('utf-8')
    roomName = db.read(b'roomName').decode('utf-8')
    if deviceName == '-1' or (roomId == '-1' and (roomName == '-1' or roomUser == '-1')):
        np.showerror()
        while readcmd.readcmd():
            pass
    else:
        break

# Main Code goes here
print("Homital Light OK~")
np.main()