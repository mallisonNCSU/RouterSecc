from gpiozero import LED
import netifaces
import RPi.GPIO as GPIO
import time
import multiprocessing
from multiprocessing import Queue
import requests
import urllib.request
from requests_html import HTMLSession
import lxml
import re
from bs4 import BeautifulSoup, NavigableString
from xpath_soup import xpath_soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_algorithm_oo import parse_algorithm
from Score import Score

g_led = LED(27)
r_led = LED(18)

def STATE_WAIT_CONNECTION():
#	print("STATE 1: wait for ethernet connection")
	g_led.off()
	r_led.toggle()
	time.sleep(0.5)

def STATE_WAIT_INPUT():
#	print("STATE 2: wait for user input")
	g_led.off()
	r_led.on()

def STATE_RUNNING():
#	print("STATE 3: machine running")

	r_led.on()
	g_led.toggle()
	time.sleep(0.5)

def STATE_COMPLETE():
#	print("STATE 4: complete")

	r_led.on()
	g_led.on()

def STATE_OFF():
	r_led.off()
	g_led.off()
try:
	import httplib
except:
	import http.client as httplib

def have_internet():
	try:
		conn = httplib.HTTPConnection(netifaces.gateways()['default'][netifaces.AF_INET][0], timeout = 5)
		try:
			conn.request("HEAD", "/")
			conn.close()
			print("yes internet")
			return True
		except:
			conn.close
			print("no internet")
			return False
	except:
		print("no internet")
		return False	

#def have_internet():
#	global i
#	i += 1
#	if i > 10 :
#		return False
#	else :
#		return True

def button_init(STATE):
	while True:
		if GPIO.input(4) == GPIO.LOW:
			print("Button Pressed")
			STATE.put(0)
			time.sleep(0.1)

def LED_init(LED_STATE):
	while True:
		if not LED_STATE.empty() :
			S = LED_STATE.get()
		if S == 0:
			STATE_WAIT_CONNECTION()
		elif S == 1:
			STATE_WAIT_INPUT()
		elif S == 2:
			STATE_RUNNING()
		elif S == 3:
			STATE_COMPLETE()
		else:
			STATE_OFF()
			break

#some initilization
STATE = Queue()
LED_STATE = Queue()
GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

STATE.put(0)
LED_STATE.put(0)
S = 0

p_LED = multiprocessing.Process(target = LED_init, args=(LED_STATE, ))
p_button = multiprocessing.Process(target = button_init, args=(STATE,))
		
p_LED.start()
p_button.start()

#where main loop begins
while True:
	if not STATE.empty() :
		S = STATE.get()

	if S==0 :	#STATE 0, wait for internet
		LED_STATE.put(0)
		while not have_internet():
			time.sleep(3)
		run_finish = False
		STATE.put(1)
		LED_STATE.put(1)
		open('Output.txt', 'w').close()
		open('/var/www/html/userinput.txt', 'w').close()

	elif S==1 :	#STATE 1, used to be wait for user input state. Now just a transition state.
		time.sleep(2) 	#replace with process & logic
		STATE.put(2)
		LED_STATE.put(2)

	elif S==2 and run_finish!=True :	#STATE 2, parsing & testing state
		parse = parse_algorithm()
		credentials = parse.bruteForce(netifaces.gateways()['default'][netifaces.AF_INET][0])
		if(credentials == 0):
			LED_STATE.put(1)
			result = 0
			while(result == 0):
				result = parse.userInput(netifaces.gateways()['default'][netifaces.AF_INET][0])
				time.sleep(1)
		LED_STATE.put(2)
		url = 'http://' + parse.tests['Credentials']['username'] + ':' + parse.tests['Credentials']['password'] + '@' + netifaces.gateways()['default'][netifaces.AF_INET][0]+'/'
		parse.run(url)
		Score.finish()
		run_finish = True
		STATE.put(3)
		LED_STATE.put(3)
		print("test complete! press button to restart.")
	else:
		if S!=3 :
		#	print (S)
			pass
		time.sleep(6)	#replace with process & logic

