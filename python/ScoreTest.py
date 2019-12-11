'''
ScoreTest takes dictionaries as they would be in various stages of parsing and
goes through the update method of the Score class, before waiting sleeptime seconds.
This is to check that the output file is being generated correctly.
'''

import time
from Score import Score
sleeptime = 2
Exampledic1 = {'Credentials': {'found':1,'username': 'admin', 'password': 'admin', 'mainPage': 1},
              'SSID': {'found': 0, 'value': 'dd-wrt', 'location': '', 'page': 'Wireless_Basic.asp'},
              'WifiPassword': {'found': 0, 'value': 'testpassword', 'location': '', 'page': 'WL_WPATable.asp'},
              'HTTPS': {'found': 0, 'value': 0, 'location': '', 'page': 'Management.asp'}, 
              'Encryption': {'found': 0, 'value': 'WPA2 Personal', 'location': '', 'page': 'WL_WPATable.asp'},
              'Remote': {'found': 0, 'value': 0, 'location': '', 'page': 'PPTP.asp'},
              'Web': {'found': 0, 'value': 1, 'location': '', 'page': 'Management.asp'},
              'UPnP': {'found': 0, 'value': '0', 'location': '', 'page': 'UPnP.asp'},
              'Port': {'found': 0, 'value': '500', 'location':'', 'page': 'Firewall.asp'},
              'Firmware': {'found': 0, 'value': '08/07/10', 'location': '', 'page': 'Wireless_Basic.asp'}}
Exampledic2 = {'Credentials': {'found':1,'username': 'admin', 'password': 'admin', 'mainPage': 1},
              'SSID': {'found': 1, 'value': 'dd-wrt', 'location': '', 'page': 'Wireless_Basic.asp'},
              'WifiPassword': {'found': 1, 'value': 'testpassword', 'location': '', 'page': 'WL_WPATable.asp'},
              'HTTPS': {'found': 1, 'value': 0, 'location': '', 'page': 'Management.asp'}, 
              'Encryption': {'found': 0, 'value': 'WPA2 Personal', 'location': '', 'page': 'WL_WPATable.asp'},
              'Remote': {'found': 0, 'value': 0, 'location': '', 'page': 'PPTP.asp'},
              'Web': {'found': 0, 'value': 1, 'location': '', 'page': 'Management.asp'},
              'UPnP': {'found': 0, 'value': '0', 'location': '', 'page': 'UPnP.asp'},
              'Port': {'found': 0, 'value': '500', 'location':'', 'page': 'Firewall.asp'},
              'Firmware': {'found': 0, 'value': '08/07/10', 'location': '', 'page': 'Wireless_Basic.asp'}}
Exampledic3 = {'Credentials': {'found':1,'username': 'admin', 'password': 'admin', 'mainPage': 1},
              'SSID': {'found': 1, 'value': 'dd-wrt', 'location': '', 'page': 'Wireless_Basic.asp'},
              'WifiPassword': {'found': 1, 'value': 'testpassword', 'location': '', 'page': 'WL_WPATable.asp'},
              'HTTPS': {'found': 1, 'value': 0, 'location': '', 'page': 'Management.asp'}, 
              'Encryption': {'found': 1, 'value': 'WPA2 Personal', 'location': '', 'page': 'WL_WPATable.asp'},
              'Remote': {'found': 1, 'value': 0, 'location': '', 'page': 'PPTP.asp'},
              'Web': {'found': 0, 'value': 1, 'location': '', 'page': 'Management.asp'},
              'UPnP': {'found': 0, 'value': '0', 'location': '', 'page': 'UPnP.asp'},
              'Port': {'found': 0, 'value': '500', 'location':'', 'page': 'Firewall.asp'},
              'Firmware': {'found': 0, 'value': '08/07/10', 'location': '', 'page': 'Wireless_Basic.asp'}}
Exampledic4 = {'Credentials': {'found':1,'username': 'admin', 'password': 'admin', 'mainPage': 1},
              'SSID': {'found': 1, 'value': 'dd-wrt', 'location': '', 'page': 'Wireless_Basic.asp'},
              'WifiPassword': {'found': 1, 'value': 'testpassword', 'location': '', 'page': 'WL_WPATable.asp'},
              'HTTPS': {'found': 1, 'value': 0, 'location': '', 'page': 'Management.asp'}, 
              'Encryption': {'found': 1, 'value': 'WPA2 Personal', 'location': '', 'page': 'WL_WPATable.asp'},
              'Remote': {'found': 1, 'value': 0, 'location': '', 'page': 'PPTP.asp'},
              'Web': {'found': 1, 'value': 1, 'location': '', 'page': 'Management.asp'},
              'UPnP': {'found': 1, 'value': '0', 'location': '', 'page': 'UPnP.asp'},
              'Port': {'found': 0, 'value': '500', 'location':'', 'page': 'Firewall.asp'},
              'Firmware': {'found': 0, 'value': '08/07/10', 'location': '', 'page': 'Wireless_Basic.asp'}}
Exampledic5 = {'Credentials': {'found':1,'username': 'admin', 'password': 'admin', 'mainPage': 1},
              'SSID': {'found': 1, 'value': 'dd-wrt', 'location': '', 'page': 'Wireless_Basic.asp'},
              'WifiPassword': {'found': 1, 'value': 'testpassword', 'location': '', 'page': 'WL_WPATable.asp'},
              'HTTPS': {'found': 0, 'value': 0, 'location': '', 'page': 'Management.asp'}, 
              'Encryption': {'found': 1, 'value': 'WPA2 Personal', 'location': '', 'page': 'WL_WPATable.asp'},
              'Remote': {'found': 1, 'value': 0, 'location': '', 'page': 'PPTP.asp'},
              'Web': {'found': 1, 'value': 1, 'location': '', 'page': 'Management.asp'},
              'UPnP': {'found': 1, 'value': '0', 'location': '', 'page': 'UPnP.asp'},
              'Port': {'found': 1, 'value': '500', 'location':'', 'page': 'Firewall.asp'},
              'Firmware': {'found': 1, 'value': '08/07/10', 'location': '', 'page': 'Wireless_Basic.asp'}}
try:
    fp = open('Output.txt', mode = 'w')
    fp.close()
except:
    pass
Score.update(Exampledic1)
print('updated')
time.sleep(sleeptime)
Score.update(Exampledic2)
print('updated')
time.sleep(sleeptime)
Score.update(Exampledic3)
print('updated')
time.sleep(sleeptime)
Score.update(Exampledic4)
print('updated')
time.sleep(sleeptime)
Score.update(Exampledic5)
print('updated')
time.sleep(sleeptime)
Score.finish()
