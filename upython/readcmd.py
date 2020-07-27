import os
import db

def readcmd():
    cmd = input('--> ').split()
    print('Cmd received:')
    print(cmd)
    if cmd[0] == 'wifi':
        ssid = cmd[1]
        pswd = cmd[2]
        db.write(b'wifissid', ssid.encode('utf-8'))
        db.write(b'wifipassword', pswd.encode('utf-8'))
        return 0
    elif cmd[0] == 'setByName':
        roomUser = cmd[1]
        roomName = cmd[2]
        deviceName = cmd[3]
        db.write(b'roomUser', roomUser.encode('utf-8'))
        db.write(b'roomName', roomName.encode('utf-8'))
        db.write(b'deviceName', deviceName.encode('utf-8'))
        return 0
    elif cmd[0] == 'setById':
        roomId = cmd[1]
        deviceName = cmd[2]
        db.write(b'roomId', roomId.encode('utf-8'))
        db.write(b'deviceName', deviceName.encode('utf-8'))
        return 0
    print('command must be one of [wifi, setBYName, setById]')
    return -1