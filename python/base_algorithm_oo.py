import requests
import urllib.request
from requests_html import HTMLSession
import time
import lxml
import re
from bs4 import BeautifulSoup, NavigableString
from xpath_soup import xpath_soup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Score import Score

'''
filelist = ['top100', 'top1000', 'top10000', 'top100000', 'top1000000']
toplist = {}

for file in filelist:
    try:
        with open(file + '.txt', mode='r') as fp:
            toplist[file] = [line.rstrip('\n') for line in fp]
        fp.close()
    except OSError:
        print('File: ' + file + '.txt' + ' failed to load.')

Tests to do:
1: Admin credentials
2: WiFi SSID
3: WiFi password
4: HTTPS
5: WPA2 enabled
6: Remote Access
7: Web Access
8: UPnP
9: Port
10: Firmware

Note: some of these tests are interdependent--eg. Port only applies if remote management is enabled,
so the scoring algorithm/UI needs to reflect that
'''

class parse_algorithm:  
    def __init__(self):
        self.stop = 0
        self.depth = 0
        self.found = 0
        self.curPage = ''
        self.token = 0
        self.tests = {
            'Credentials': {
                'found': 0,
                'username': '',
                'password': '',
                'mainPage': 0
            },
            'SSID': {
                'found': 0,
                'value': '',
                'location': '',
                'page': ''
            },
            'WifiPassword': {
                'found': 0,
                'value': '',
                'location': '',
                'page': ''
            },
            'HTTPS': {
                'found': 0,
                'value': '',
                'location': '',
                'page': ''
            },
            'Encryption': {
                'found': 0,
                'value': '',
                'location': '',
                'page': ''
            },
            'Remote': {
                'found': 0,
                'value': '',
                'location': '',
                'page': ''
            },
            'Web': {
                'found': 0,
                'value': '',
                'location': '',
                'page': ''
            },
            'UPnP': {
                'found': 0,
                'value': '',
                'location': '',
                'page': ''
            },
            'Port': {
                'found': 0,
                'value': '',
                'location': '',
                'page': ''
            },
            'Firmware': {
                'found': 0,
                'value': '',
                'location': '',
                'page': ''
            }
        }
        
    def userInput(self, gateway):
        gateway = gateway + '/'

        try:
            with open('/var/www/html/userinput.txt', mode='r') as fp:
                credentials = [line.rstrip('\n') for line in fp]
                fp.close()
        except OSError:
            print('File: ' + file + '.txt' + ' failed to load.')
        if(len(credentials) is not 0):
                    if(self.token != credentials[2]):
                            self.token = credentials[2]
                            session = HTMLSession()
                            print('Trying custom credentials: User: ' + credentials[0] + ' Password: ' + credentials[1])
                            r = session.get('http://'+ credentials[0] + ':' + credentials[1] + '@' + gateway)
                            print('http://' + credentials[0] + ':' + credentials[1] + '@'+ gateway)
                            code = r.status_code
                            print('Response: ' + str(code))
                            if(code != 200 and self.tests['Credentials']['mainPage'] == 1):
                                    print('Trying subpage...')
                                    r.html.render()
                                    soup = BeautifulSoup(r.html.html, 'lxml')
                                    page = soup.find('a')
                                    print('http://' + credentials[0] + ':' + credentials[1] + '@'+ gateway + page['href'])
                                    r = session.get('http://' + credentials[0] + ':' + credentials[1] + '@' + gateway + page['href'])
                                    code = r.status_code
                                    print('Response: ' + str(code))
                                    if (code == 200):
                                            self.tests['Credentials']['username'] = credentials[0]
                                            self.tests['Credentials']['password'] = credentials[1]
                                            try:
                                                    Score.update(self.tests)
                                                    self.tests['Credentials']['found'] = 1
                                            except:
                                                    pass
                                            session.close()
                                            return 1
                                    else:
                                            print('Custom credentials incorrect. Waiting for new input...')
                                            return 0
                            else:
                                    if(code == 200):
                                            self.tests['Credentials']['username'] = credentials[0]
                                            self.tests['Credentials']['password'] = credentials[1]
                                            try:
                                                    Score.update(self.tests)
                                                    self.tests['Credentials']['found'] = 1
                                            except:
                                                    pass
                                            session.close()
                                            return 1
                                    else:
                                        print('Custom credentials incorrect. Waiting for new input...')
                                        return 0
                    else:
                            return 0
        else: return 0


    def bruteForce(self, gateway):
        filelist = ['top100', 'top1000', 'top10000', 'top100000', 'top1000000']
        toplist = {}
        defaultUsernames = {}
        defaultPasswords = {}
        gateway = gateway + '/'

        for file in filelist:
            try:
                with open(file + '.txt', mode='r') as fp:
                    toplist[file] = [line.rstrip('\n') for line in fp]
                fp.close()
            except OSError:
                print('File: ' + file + '.txt' + ' failed to load.')
        
        try:
            with open('usernames.txt', mode='r') as fp:
                defaultUsernames = [line.rstrip('\n') for line in fp]
            fp.close()
        except OSError:
            print('File: usernames.txt failed to load.')
            
        try:
            with open('passwords.txt', mode='r') as fp:
                defaultPasswords = [line.rstrip('\n') for line in fp]
            fp.close()
        except OSError:
            print('File: usernames.txt failed to load.')
        
        session = HTMLSession()
        print('Trying no credentials...')
        r = session.get('http://' + gateway)
        code = r.status_code
        print('Response: ' + str(code))
        if(code == 200):
            print('Trying subpage...')
            r.html.render()
            soup = BeautifulSoup(r.html.html, 'lxml')
            page = soup.find('a')
            r = session.get('http://' + gateway + page['href'])
            code = r.status_code
            print('Response: ' + str(code))
            if (code == 200):
                self.tests['Credentials']['username'] = ''
                self.tests['Credentials']['password'] = ''
                self.tests['Credentials']['mainPage'] = 0
                try:
                    Score.update(self.tests)
                    self.tests['Credentials']['found'] = 1
                except:
                    pass
                session.close()
                return 1
            else:
                self.tests['Credentials']['mainPage'] = 1
        else:
            self.tests['Credentials']['mainPage'] = 0
            
        for user in defaultUsernames:
            for password in defaultPasswords:
                print('\nTrying credentials:\n' + 'User: ' + user + '\n' + 'Password: ' + password)
                if (self.tests['Credentials']['mainPage']):
                    url = 'http://' + user + ':' + password + '@' + gateway + page['href']
                else:
                    url = 'http://' + user + ':' + password + '@' + gateway
                r = session.get(url)
                code = r.status_code
                print('Response: ' + str(code))
                if(code == 200):
                    self.tests['Credentials']['username'] = user
                    self.tests['Credentials']['password'] = password
                    try:
                        Score.update(self.tests)
                        self.tests['Credentials']['found'] = 1

                    except:
                        pass
                    session.close()
                    return 1
                    
        for user in defaultUsernames:
            for password in toplist['top100']:
                print('\nTrying credentials:\n' + 'User: ' + user + '\n' + 'Password: ' + password)
                if (self.tests['Credentials']['mainPage']):
                    url = 'http://' + user + ':' + password + '@' + gateway + page['href']
                else:
                    url = 'http://' + user + ':' + password + '@' + gateway
                r = session.get(url)
                code = r.status_code
                print('Response: ' + str(code))
                if(code == 200):
                    self.tests['Credentials']['username'] = user
                    self.tests['Credentials']['password'] = password
                    try:
                        Score.update(self.tests)
                        self.tests['Credentials']['found'] = 1

                    except:
                        pass
                    session.close()
                    return 1
        
        print('Could not find admin credentials. Waiting for user input.')
        
        return 0
        
    def checkTag(self, tag, test):
        if (test == 2 and not self.tests['SSID']['found']): #check for input AND text
            if(tag.name == 'input' and not (tag.attrs.get('type') in ['button', 'hidden', 'image', 'radio'])):
                print(tag)
                print('SSID: ' + tag['value'])
                self.tests['SSID']['found'] = 1
                self.tests['SSID']['value'] = tag['value']
                self.tests['SSID']['location'] = tag
                self.tests['SSID']['page'] = self.curPage
                self.found = self.found + 1
                try:
                    Score.update(self.tests)
                except:
                    pass
                return 1
            return 0
        
        if (test == 3 and not self.tests['WifiPassword']['found']): #check for input AND text?
            if(tag.name == 'input' and not (tag.attrs.get('type') in ['button', 'hidden', 'image'])):
                print(tag)
                print('WifiPassword: ' + tag['value'])
                self.tests['WifiPassword']['found'] = 1
                self.tests['WifiPassword']['value'] = tag['value']
                self.tests['WifiPassword']['location'] = tag
                self.tests['WifiPassword']['page'] = self.curPage
                self.found = self.found + 1
                try:
                    Score.update(self.tests)
                except:
                    pass
                return 1
            return 0
        
        
        if (test == 4 and not self.tests['HTTPS']['found']): #check for input AND text?
            if(tag.name == 'input' and (tag.attrs.get('type') in ['checkbox']) and ('name' in tag.attrs) and ('https' in tag['name'])):
                print(tag)
                print('HTTPS: ' + tag['value'])
                self.tests['HTTPS']['found'] = 1
                if('checked' in tag.attrs):
                    self.tests['HTTPS']['value'] = 1
                else:
                    self.tests['HTTPS']['value'] = 0
                self.tests['HTTPS']['location'] = tag
                self.tests['HTTPS']['page'] = self.curPage
                self.found = self.found + 1
                try:
                    Score.update(self.tests)
                except:
                    pass
                return 1
            return 0
        
        
        if (test == 5 and not self.tests['Encryption']['found']): #dropdown? radio buttons?
            if(tag.name == 'option'):
                if('selected' in tag.attrs):
                    if (tag.string):
                        text = tag.string
                    else:
                        inner_text = [element for element in tag if isinstance(element, NavigableString)]
                        text = ''.join(inner_text)
                    print(tag)
                    print('Encryption: ' + text)
                    self.tests['Encryption']['found'] = 1
                    self.tests['Encryption']['value'] = text
                    self.tests['Encryption']['location'] = tag
                    self.tests['Encryption']['page'] = self.curPage
                    self.found = self.found + 1
                    try:
                        Score.update(self.tests)
                    except:
                        pass
                    return 1
            return 0
        
        if (test == 6 and not self.tests['Remote']['found']): #remote
            if(tag.name == 'input' and not (tag.attrs.get('type') in ['button', 'hidden', 'image']) and ('name' in tag.attrs) and ('remote' in tag['name'])):
                print(tag)
                self.tests['Remote']['found'] = 1
                if('checked' in tag.attrs):
                    self.tests['Remote']['value'] = 1
                else:
                    self.tests['Remote']['value'] = 0
                self.tests['Remote']['location'] = tag
                self.tests['Remote']['page'] = self.curPage
                self.found = self.found + 1
                try:
                    Score.update(self.tests)
                except:
                    pass
                return 1
            return 0
        
        
        if (test == 7 and not self.tests['Web']['found']): #remote
            if(tag.name == 'input' and (tag.attrs.get('type') in ['radio'])):
                print(tag)
                self.tests['Web']['found'] = 1
                if('checked' in tag.attrs):
                    self.tests['Web']['value'] = 1
                else:
                    self.tests['Web']['value'] = 0
                self.tests['Web']['location'] = tag
                self.tests['Web']['page'] = self.curPage
                self.found = self.found + 1
                try:
                    Score.update(self.tests)
                except:
                    pass
                return 1
            return 0
        
        
        if (test == 8 and not self.tests['UPnP']['found']): #radio buttons probably. might need to look for "enable"/"disable" text
            if(tag.name == 'input' and not (tag.attrs.get('type') in ['button', 'hidden', 'image'])):
                if('checked' in tag.attrs):
                    print(tag)
                    print('UPnP: ' + tag['value'])
                    self.tests['UPnP']['found'] = 1
                    self.tests['UPnP']['value'] = tag['value']
                    self.tests['UPnP']['location'] = tag
                    self.tests['UPnP']['page'] = self.curPage
                    self.found = self.found + 1
                    try:
                        Score.update(self.tests)
                    except:
                        pass
                    return 1
            return 0
        
        if (test == 9): #check for text, maybe input?
            if(tag.name == 'input' and (not (tag.attrs.get('type') in ['button', 'radio', 'checkbox', 'hidden', 'image']))):
                if(tag['value'].isdigit()):
                    print(tag)
                    print('Port: ' + tag['value'])
                    self.tests['Port']['found'] = 1
                    self.tests['Port']['value'] = tag['value']
                    self.tests['Port']['location'] = tag
                    self.tests['Port']['page'] = self.curPage
                    self.found = self.found + 1
                    try:
                        Score.update(self.tests)
                    except:
                        pass
                    return 1
            return 0
            
        if (test == 10): #check for text, maybe input?
            p = re.compile('\d\d/\d\d/\d\d')
            date = p.search(str(tag.string))
            if date:
                print(date.group(0))
                self.tests['Firmware']['found'] = 1
                self.tests['Firmware']['value'] = date.group(0)
                self.tests['Firmware']['location'] = tag
                self.tests['Firmware']['page'] = self.curPage
                self.found = self.found + 1
                try:
                    Score.update(self.tests)
                except:
                    pass
                return 1
            return 0
        
        
    def searchChildren(self, target, test):
        targetDescendants = target.descendants
        for desc in targetDescendants:
            if self.stop: return
            if(desc.name): #every other entry in list is blank
                tagFound = self.checkTag(desc, test)
                if (tagFound):
                    self.stop = 1
                    return
                
        
    def searchSib(self, target, test):
        if(self.depth > 6): #this is where the maximum depth is 
            return
        self.depth = self.depth + 1
        #print(target)
        tagFound = self.checkTag(target, test)
        if (tagFound):
            self.stop = 1
            return
        if(target.next_sibling):
            targetSiblings = target.next_siblings
            for sib in targetSiblings:
                if self.stop: return
                if(sib.name): #every other entry in list is blank
                    tagFound = self.checkTag(sib, test)
                    if (tagFound):
                        self.stop = 1
                        return
                    #print(sib.name)
                    self.searchChildren(sib, test)
        self.searchSib(target.parent, test)
                
                
    def searchSetting(self, page):
        allBody = page.find('body')
        self.stop = 0
        self.depth = 0
        #test2: SSID
        if(not self.tests['SSID']['found']):
            textLoc = allBody.findAll(string=re.compile('SSID'))
            #print(textLoc)
            for loc in textLoc:
                actualLoc = loc.parent
                if self.stop: break
                if(actualLoc.name):
                    #print(actualLoc)
                    self.searchChildren(actualLoc, 2)
                    self.depth = 0
                    self.searchSib(actualLoc, 2)
                    self.depth = 0
            self.stop = 0
            self.depth = 0
            
        #test3: WiFi Password
        if(not self.tests['WifiPassword']['found']):
            textLoc = allBody.findAll(string=re.compile('WPA Shared')) #isn't "WPA Shared Key" because linksys is stupid
            textLoc.extend(allBody.findAll(string=re.compile('Passphrase')))
            print(textLoc)
            for loc in textLoc:
                actualLoc = loc.parent
                if self.stop: break
                if(actualLoc.name):
                    #print(actualLoc)
                    self.searchChildren(actualLoc, 3)
                    self.depth = 0
                    self.searchSib(actualLoc, 3)
                    self.depth = 0
            self.stop = 0
            self.depth = 0
            
        #test4: HTTPS
        if(not self.tests['HTTPS']['found']):
            textLoc = allBody.findAll(string=re.compile('HTTP')) #isn't "WPA Shared Key" because linksys is stupid
            print(textLoc)
            for loc in textLoc:
                actualLoc = loc.parent
                if self.stop: break
                if(actualLoc.name and (actualLoc.name != 'script')):
                    #print(actualLoc)
                    self.searchChildren(actualLoc, 4)
                    self.depth = 0
                    self.searchSib(actualLoc, 4)
                    self.depth = 0
            self.stop = 0
            self.depth = 0
            
        #test5: WPA2 Enabled - "Encryption"
        if(not self.tests['Encryption']['found']):
            textLoc = allBody.findAll(string=re.compile('Security Mode'))
            print(textLoc)
            for loc in textLoc:
                actualLoc = loc.parent
                if self.stop: break
                if(actualLoc.name):
                    #print(actualLoc)
                    self.searchChildren(actualLoc, 5)
                    self.depth = 0
                    self.searchSib(actualLoc, 5)
                    self.depth = 0
            self.stop = 0
            self.depth = 0
            
        #test6: Remote
        if(not self.tests['Remote']['found']):
            textLoc = allBody.findAll(string=re.compile('Remote'))
            print(textLoc)
            for loc in textLoc:
                actualLoc = loc.parent
                if self.stop: break
                if(actualLoc.name):
                    #print(actualLoc)
                    self.searchChildren(actualLoc, 6)
                    self.depth = 0
                    self.searchSib(actualLoc, 6)
                    self.depth = 0
            self.stop = 0
            self.depth = 0
            
        #test7: Web
        if(not self.tests['Web']['found']):
            textLoc = allBody.findAll(string=re.compile('Web Access'))
            textLoc.extend(allBody.findAll(string=re.compile('Local Management')))
            print(textLoc)
            for loc in textLoc:
                actualLoc = loc.parent
                if self.stop: break
                if(actualLoc.name):
                    #print(actualLoc)
                    self.searchChildren(actualLoc, 7)
                    self.depth = 0
                    self.searchSib(actualLoc, 7)
                    self.depth = 0
            self.stop = 0
            self.depth = 0
            
        #test8: UPnP
        if(not self.tests['UPnP']['found']):
            textLoc = allBody.findAll(string=re.compile('UPnP'))
            print(textLoc)
            for loc in textLoc:
                actualLoc = loc.parent
                if self.stop: break
                if(actualLoc.name):
                    #print(actualLoc)
                    self.searchChildren(actualLoc, 8)
                    self.depth = 0
                    self.searchSib(actualLoc, 8)
                    self.depth = 0
            self.stop = 0
            self.depth = 0
            
        #test9: Port
        if(not self.tests['Port']['found']):
            textLoc = allBody.findAll(string=re.compile('Port'))
            print(textLoc)
            for loc in textLoc:
                actualLoc = loc.parent
                if self.stop: break
                if(actualLoc.name):
                    #print(actualLoc)
                    self.searchChildren(actualLoc, 9)
                    self.depth = 0
                    self.searchSib(actualLoc, 9)
                    self.depth = 0
            self.stop = 0
            self.depth = 0
            
        #test10: Firmware
        if(not self.tests['Firmware']['found']):
            textLoc = allBody.findAll(string=re.compile('Firmware'))
            print(textLoc)
            for loc in textLoc:
                actualLoc = loc.parent
                if self.stop: break
                if(actualLoc.name):
                    #print(actualLoc)
                    self.searchChildren(actualLoc, 10)
                    self.depth = 0
                    self.searchSib(actualLoc, 10)
                    self.depth = 0
            self.stop = 0
            self.depth = 0
        
    
    def run(self,url): #'http://admin:admin@192.168.1.1'
        print('**Creating session...')
        session = HTMLSession()
        self.stop = 0
        self.depth = 0
        self.found = 0
            
        print('**Accessing admin portal...')
        r = session.get(url)
        print('**Rendering webpage...')
        r.html.render()
        print('**Retrieving webpage source...')
        soup = BeautifulSoup(r.html.html, 'lxml')

        print('**Forming list of pages...')
        iPageTable = soup.findAll('a')
        pageTable = []

        for page in iPageTable:
            pageTable.append(page['href'])

        pageTable = [page for page in pageTable if 'http' not in page]
        pageTable = [page for page in pageTable if 'javascript' not in page]
        pageTable = list(set(pageTable))

        for page in pageTable:
            print(page)
            
        for page in pageTable:
            if(self.found < len(self.tests)):
                r = session.get(url + page)
                r.html.render()
                print(page)
                self.curPage = page
                newPage = BeautifulSoup(r.html.html, 'lxml')
                self.searchSetting(newPage)
                
                iSubPageTable = newPage.findAll('a')
                subPageTable = []
                print(page)
                for subPage in iSubPageTable:
                    subPageTable.append(subPage['href'])
                subPageTable = [subPage for subPage in subPageTable if 'http' not in subPage]
                subPageTable = [subPage for subPage in subPageTable if 'javascript' not in subPage]
                subPageTable = list(set(subPageTable))
                for subPage in subPageTable:
                    print(subPage)
                
                for subPage in subPageTable:
                    if((self.found < (len(self.tests)-1)) and (subPage not in pageTable)):
                        r = session.get(url + subPage)
                        r.html.render()
                        print(subPage)
                        self.curPage = subPage
                        newSubPage = BeautifulSoup(r.html.html, 'lxml')
                        self.searchSetting(newSubPage)
        session.close()

        print('------SSID------')
        print('Found: ' + str(self.tests['SSID']['found']) + '\nValue: ' + str(self.tests['SSID']['value']) + '\nLocation: ' + str(self.tests['SSID']['location'])+ '\nPage: ' + str(self.tests['SSID']['page']))
        print('------WifiPassword------')
        print('Found: ' + str(self.tests['WifiPassword']['found']) + '\nValue: ' + str(self.tests['WifiPassword']['value']) + '\nLocation: ' + str(self.tests['WifiPassword']['location'])+ '\nPage: ' + str(self.tests['WifiPassword']['page']))
        print('------HTTPS------')
        print('Found: ' + str(self.tests['HTTPS']['found']) + '\nValue: ' + str(self.tests['HTTPS']['value']) + '\nLocation: ' + str(self.tests['HTTPS']['location'])+ '\nPage: ' + str(self.tests['HTTPS']['page']))
        print('------Encryption------')
        print('Found: ' + str(self.tests['Encryption']['found']) + '\nValue: ' + str(self.tests['Encryption']['value']) + '\nLocation: ' + str(self.tests['Encryption']['location'])+ '\nPage: ' + str(self.tests['Encryption']['page']))
        print('------Remote------')
        print('Found: ' + str(self.tests['Remote']['found']) + '\nValue: ' + str(self.tests['Remote']['value']) + '\nLocation: ' + str(self.tests['Remote']['location'])+ '\nPage: ' + str(self.tests['Remote']['page']))
        print('------Web------')
        print('Found: ' + str(self.tests['Web']['found']) + '\nValue: ' + str(self.tests['Web']['value']) + '\nLocation: ' + str(self.tests['Web']['location'])+ '\nPage: ' + str(self.tests['Web']['page']))
        print('------UPnP------')
        print('Found: ' + str(self.tests['UPnP']['found']) + '\nValue: ' + str(self.tests['UPnP']['value']) + '\nLocation: ' + str(self.tests['UPnP']['location'])+ '\nPage: ' + str(self.tests['UPnP']['page']))
        print('------Port------')
        print('Found: ' + str(self.tests['Port']['found']) + '\nValue: ' + str(self.tests['Port']['value']) + '\nLocation: ' + str(self.tests['Port']['location'])+ '\nPage: ' + str(self.tests['Port']['page']))
        print('------Firmware------')
        print('Found: ' + str(self.tests['Firmware']['found']) + '\nValue: ' + str(self.tests['Firmware']['value']) + '\nLocation: ' + str(self.tests['Firmware']['location'])+ '\nPage: ' + str(self.tests['Firmware']['page']))
