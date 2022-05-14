import sys
import json
import argparse
import socket
import struct
import time
import re
from unicodedata import name
import requests
import configparser
from pypresence import Presence

config = configparser.ConfigParser()
config.read('settings.ini')
ip = config['main']['ip']
clientid = config['main']['clientid']

TCP_PORT = 0xCAFE
PACKETMAGIC = 0xFFAADD23

parser = argparse.ArgumentParser()
parser.add_argument('--ignore-home-screen', dest='ignore_home_screen', action='store_true', help='Don\'t display the home screen. Defaults to false if missing this flag.')

#Defines a title packet
class Title:

    def __init__(self, raw_data):
        unpacker = struct.Struct('4L612s')
        enc_data = unpacker.unpack(raw_data)
        self.magic = int(enc_data[0])
        #print(enc_data)
        if int(enc_data[3]) == 0:
            self.pid = int(enc_data[1])
            self.name = 'Home Menu'
            self.url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Nintendo_Switch_Logo_%28without_text%29.svg/480px-Nintendo_Switch_Logo_%28without_text%29.svg.png'
        else:
            self.pid = int(enc_data[1])
            self.name = enc_data[4].decode('utf-8', 'ignore').split('\x00')[0]
            self.url = "https://assets.nintendo.com/image/upload/ar_1.0,c_scale,g_north_west,w_350/v1/ncom/en_US/games/switch/%s/%s-switch/hero" %(self.name[0], format(self.name).replace(' ', '-'))


def main():
    consoleargs = parser.parse_args()
    switch_ip = ip

    if not checkIP(switch_ip):
        print('Invalid IP')
        exit()

    rpc = Presence(str(clientid))
    try:
        rpc.connect()
        rpc.clear()
    except:
        print('Unable to start RPC!')

    switch_server_address = (switch_ip, TCP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(switch_server_address)
        print('Successfully connected to %s' % switch_ip + ':' + str(TCP_PORT))
    except:
        print('Error connection to %s refused' % switch_ip + ':' + str(TCP_PORT))
        exit()

    lastProgramName = ''
    startTimer = 0

    while True:
        data = None
        try:
            data = sock.recv(628)
        except:
            print('Could not connect to Server! Retrying...')
            startTimer = 0
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect(switch_server_address)
                print('Successfully reconnected to %s' %
                      repr(switch_server_address))
            except:
                print('Error reconnection to %s refused' %
                      repr(switch_server_address))
                exit()
        title = Title(data)
        if title.magic == PACKETMAGIC:
            if lastProgramName != title.name:
                startTimer = int(time.time())
                print("Now playing", title.name)
            if consoleargs.ignore_home_screen and title.name == 'Home Menu':
                rpc.clear()
            else:
                smallimagetext = ''
                largeimagekey = ''
                details = ''
                largeimagetext = title.name
                if int(title.pid) != PACKETMAGIC:
                    smallimagetext = 'SwitchPresence-Rewritten'
                    largeimagekey = iconFromPid(title.pid)
                    details = 'Playing ' + str(title.name)
                if not title.name:
                    title.name = ''
                lastProgramName = title.name
                rpc.update(details=details, start=startTimer, large_image=title.url,
                        large_text=largeimagetext, small_text=smallimagetext)
            time.sleep(1)
        else:
            print("Closing...")
            time.sleep(1)
            rpc.clear()
            rpc.close()
            sock.close()
            exit()

# uses regex to validate ip
def checkIP(ip):
    regex = r'''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
    return re.search(regex, ip)

def iconFromPid(pid):
    return '0' + str(hex(int(pid))).split('0x')[1]


if __name__ == '__main__':
    main()