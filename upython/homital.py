import db
import machine
try:
    import urequests as requests
except:
    import requests

SERVER_ADDR = 'http://homital.ml:2333/api'
TOKEN = 'homital'

def isConnected():
    try:
        res = requests.get(SERVER_ADDR + '/device', headers={'Authorization':'Bearer ' + TOKEN})
        if res.status_code != 200:
            res.close()
            return False
        rj = res.json()
        res.close()
        return rj == 'authorized!'
    except:
        return False

def getRoomId(username, roomname):
    try:
        url = SERVER_ADDR + '/device/roomid' + '?username=%s&roomname=%s'%(username,roomname)
        res = requests.get(url,headers={'Authorization':'Bearer ' + TOKEN})
        if res.status_code != 200:
            res.close()
            return {'success': False}
        rj = res.json()
        res.close()
        return {'success': True, 'uid': rj['uid']}
    except:
        return {'success': False}

def getStatus():
    try:
        roomId = db.read(b'roomId').decode('utf-8')
        deviceName = db.read(b'deviceName').decode('utf-8')
        if deviceName == '-1':
            machine.reset()
        if roomId == '-1':
            roomUser = db.read(b'roomUser').decode('utf-8')
            roomName = db.read(b'roomName').decode('utf-8')
            if roomUser == '-1' or roomName == '-1':
                machine.reset()
            else:
                gid = getRoomId(roomUser, roomName)
                if gid['success']:
                    print('uid: %s'%(gid['uid'],))
                    db.write(b'roomId', gid['uid'].encode('utf-8'))
                    roomId = db.read(b'roomId').decode('utf-8')
                else:
                    print('getid failed')
        if roomId == '-1':
            machine.reset()
        url = SERVER_ADDR + '/device/status' + '?uid=%s&devicename=%s'%(roomId,deviceName)
        # print(url)
        res = requests.get(url,headers={'Authorization':'Bearer ' + TOKEN})
        if res.status_code != 200:
            print('Err: status %d, msg %s' % (res.status_code, str(res.json())))
            res.close()
            return {'success': False}
        rj = res.json()
        res.close()
        return {'success': True, 'status': rj}
    except Exception as e:
        print('Err:')
        print(e)
        return {'success': False}

def checkForUpdate():
    print("Currently running Homital-L0 %s" % ('1.0.0'))
    print("Searching for updates...")
    try:
        res = requests.get(SERVER_ADDR + '/device/updates/homital-l0', headers={'Authorization':'Bearer ' + TOKEN})
        rj = res.json()
        res.close()
        if rj['success'] == True:
            print('Versions available:')
            rj['versions'].sort() #only work for single number versions
            for v in rj['versions']:
                print("  %s" % (v,))
            if rj['versions'][-1] > '1.0.0':
                print("New version available: %s" % (rj['versions'][-1],))
                print("But sadly I cannot automatically install the update yet :<")
                print("You can try installing the update yourself")
                print("See %s" % ("https://github.com/Homital/Homital-L0"))
            else:
                print("Already running the latest version!")
    except:
        print("Something went wrong when checking for updates, skipping...")

#Download the update and replace the existing script... (better keep a backup)
#Update version number in db
def fetchUpdate(version):
    print("Updating to %s..." % (version))