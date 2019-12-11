"""
MODULES TO INSTALL:
-password-strength
"""
import sys
import time
from password_strength import PasswordStats
class Score:
    #Set first pass of Score class
    FDict = {}
    firstrun = True
    filelist = ['top100', 'top1000', 'top10000', 'top100000', 'top1000000']
    # Dictionaries
    testWeights = {
        'Credentials':  .2,
        #string
        #mainpage is binary 1bad 0 good
        'SSID':         .08, #string
        'WifiPassword': .1,  #string
        'HTTPS':        .05, #1 https, 0 http
        'Encryption':   .15, #WPA2
        'Remote':       .1,  #01
        'Web':          .05, #01
        'UPnP':         .03, #01
        'Port':         .01,
        'Firmware':     .15  #01
    #need to be added to tests, format may change
    ##    'DNS':.12,
        }
    passwordWeights = {
        'top100':.0125,
        'top1000':.025,
        'top10000':.05,
        'top100000':.1,
        'top1000000':.15,
        'None':.8
        }
    credentialWeights = {
        'username':.2 ,
        'password':.6 ,
        'mainPage':.2
        }
    SSID_defaults = ['Linksys','Cisco','D-link','Netgear','TP-Link','Google','Asus','Synology']
    names = {
        'Credentials':  't1_score',
        'SSID':         't6_score',
        'WifiPassword': 't4_score',
        'HTTPS':        't7_score',
        'Encryption':   't2_score',
        'Remote':       't5_score',
        'Web':          't8_score',
        'UPnP':         't9_score',
        'Port':         't10_score',
        'Firmware':     't3_score'
        }
    #returns the credential score
    def credential(cdic):
        string = ''
        Mpage = cdic['mainPage']
        user = cdic['username']
        upass = cdic['password']
        score = 1.0
        if cdic['mainPage'] == 1:
            score = score - Score.credentialWeights['mainPage']
        if user == 'admin' and upass == 'admin':
            score = score - Score.credentialWeights['password']
            string = 'Default login credentials. -very insecure.'
        else:
            scre,top = Score.checkpass(upass)
            if top in Score.filelist:
                string = 'Password appears in a list of the top ' + top[3:] + ' passwords.'
            score = score - (1 - scre)
        if string == '':
            string = 'Password does not appear in common password lists. It is fairly secure.'
        return score, string
            
    #generate score for general password
    def checkpass(passStat):
        score = 0.0
        check,points = Score.passTry(passStat)
        score = score + Score.passwordWeights[check]
        score = score + 0.2*points
        return score, check

    #Open and check each password in the list in a file with a given password
    def passTry(passStat):
        Stat = PasswordStats(passStat)
        passwordweak ='None'
        for file in Score.filelist:
            try:
                with open(file + '.txt', mode='r') as fp:
                    for line in fp:
                        if passStat == line.rstrip('\n'):
                            passwordweak = file
                            fp.close()
                            return passwordweak, Stat.strength()
                fp.close()
            except OSError:
                print('File: ' + file + '.txt' + ' failed to load.')
        return passwordweak, Stat.strength()
    
    #calculation function for SSID
    def cSSID(Tdic):
        ssid_score = 1.0
        string = ''
        for c in Score.SSID_defaults:
            if c in Tdic['value']:
                ssid_score = 0.5
                string = 'Your SSID is using a default name: ' + str(c)
                break
        if string == '':
            string = 'The SSID is using a name that does not have common features. This is good.'
        return ssid_score, string
    
    #calculation function for WifiPassword  
    def cWifiPassword(Tdic):
        string = ''
        wifi_score,check = Score.checkpass(Tdic['value'])
        if check != 'None':
            string = 'Wifi password appears in a list of the top ' + check[3:] + ' passwords.'
        if string == '':
            string = 'Wifi password does not appear in common password lists.'
        return wifi_score, string
        
    #calculation function for HTTPS
    def cHTTPS(Tdic):
        string = ''
        http = Tdic['value']
        if http == 1:
            http_score = 1.0
            string = 'HTTPS is enabled in your router settings, which is good, \
information passing through the router will be much harder to decode.'
        else:
            http_score = 0.5
            string = 'HTTPS is not enabled in your router settings. \
Enabling HTTPS will increase the security of packets being sent by the router.'
        return http_score, string

    #calculation function for Encryption
    def cEncryption(Tdic):
        encrypt = Tdic['value']
        string = ''
        if 'WPA2' in encrypt:
            encrypt_score = 1.0
            string = 'WPA2 is enabled. WPA2 is a good type of encryption.'
        else:
            encrypt_score = 0.4
            string = 'WPA2 is not enabled. Consider changing this setting, \
as your information will be more secure if it is encrypted with WPA2.'
        return encrypt_score, string
    
    #calculation function for Remote
    def cRemote(Tdic):
        remote = Tdic['value']
        string = ''
        if remote == 1:
            remote_score = 1.0
            string = 'Remote access enabled is not enabled on your router. \
This means that people cannout access your router settings without being directly \
on the routers network, preventing unwanted webaccess.'
        else:
            remote_score = 0.3
            string = "Remote access is enabled on your router. This means that people outside your \
routers network can potentially access and change your routers settings."
        return remote_score, string

    #calculation function for Web
    def cWeb(Tdic):
        string = ''
        web = Tdic['value']
        if web == 1:
            web_score = 1.0
            string = 'Web access is not enabled on your router.'
        else:
            web_score = 0.3
            string = 'Web access is enabled on your router.'
        return web_score, string

    #calculation function for UPnP
    def cUPnP(Tdic):
        upnp = Tdic['value']
        string = ''
        if upnp == 1:
            upnp_score = 1.0
            string = 'UPnP is not enabled. This means that it will be more difficult for someone \
to find an open port on your router.'
        else:
            upnp_score = 0.3
            string = 'UPnP is enabled. This means that devices on the network will be able \
to discover other devices on the network.'
        return upnp_score, string

    #calculation funciton for Firmware
    #TODO implement test for firmware version based on time.
    def cFirmware(Tdic):
        firm = Tdic['value']
        string = 'Firmware has been updated in the past year.'
        firm_score = 1.0
        return firm_score, string

    #calculation function for Port
    def cPort(Tdic):
        string = ''
        port = Tdic['value']
        if port == 1:
            port_score = 1.0
            string = 'The admin portal is harder to find when it cannot be found at every port.'
        else:
            port_score = 0.4
            string = 'The admin portal is easier to find when it can be found at a default port.'
        return port_score, string

    #dictionary of functions for use in in the update function
    calculate = {
        'Credentials':  credential,
        'SSID':         cSSID,
        'WifiPassword': cWifiPassword,
        'HTTPS':        cHTTPS,
        'Encryption':   cEncryption,
        'Remote':       cRemote,
        'Web':          cWeb,
        'UPnP':         cUPnP,
        'Port':         cPort,
        'Firmware':     cFirmware
        }
    
    def update(Tdic):
        Outlist = []
        try:
            with open('Output.txt', mode='r') as fp:
            # Go line by line, strip newline character, and split string between :'s taking first split
                Outlist = [line.split(':',1)[0] for line in fp]
        except:
            e = sys.exc_info()[0]
            print('error reading file: ')
            print(e)
        #Write the score of each credential to the file
        for i in Tdic:
            if Tdic[i]['found'] == 1 and Score.names[i] not in Outlist:
                #print(i)
                score,string = Score.calculate[i](Tdic[i])
                try:
                    with open('Output.txt', mode='a') as fp:
                        fp.write(Score.names[i] + ':' + str(score) + ':' + string + '\n')
                except:
                    e = sys.exc_info()[0]
                    print('error writing to file: ')
                    print(e)
        Score.FDict = Tdic
        return

    def finish():
        Fscore = 0.0
        try:
            with open('Output.txt', mode='r') as fp:
                Outlist = [line.split(':',1)[0] for line in fp]
                if 't_score' in Outlist:
                    return
        except:
            e = sys.exc_info()[0]
            print('error writing to file: ')
            print(e) 
        for i in Score.FDict:
            score,string = Score.calculate[i](Score.FDict[i])
            Fscore = Fscore + score*Score.testWeights[i]
        try:
            with open('Output.txt', mode='a') as fp:
                fp.write('t_score' + ':' + str(Fscore) + '\n')
        except:
            e = sys.exc_info()[0]
            print('error writing to file: ')
            print(e)
        for i in Score.FDict:
            if Score.FDict[i]['found'] == 0:
                try:
                    with open('Output.txt', mode='a') as fp:
                        fp.write(Score.names[i] + ':' + 'fail'+ ':' + 'Did Not Test' + '\n')
                except:
                    e = sys.exc_info()[0]
                    print('error writing to file: ')
                    print(e)
        return

total = float(0)
for c in Score.testWeights:
    total = total + Score.testWeights[c]
print('Maximum Score Weight')
print(total)
