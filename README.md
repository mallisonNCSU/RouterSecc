# RouterSecc - Router Security Tester
## Introduction
RouterSecc - Router Security Tester is a project aimed to help people check the settings in their home routers for potential security concerns. It's aimed for easy usage even for non-tech-savvy people who are not familar with downloading or installing software.
## Requirements
This project is based on the Raspberry Pi model 3B. The Raspberry Pi needs to connect to a wireless router's LAN interface with an ethernet cable to perform tests on it.

In particular you need:
1. A Raspberry Pi model 3B running Raspbian, the download and installation guide can be found from [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
2. Python 3.6+, which can be downloaded from [python.org](https://www.python.org/downloads/source/)
3. Apache 2.0+, whch can be downloaded from [apache.org](https://httpd.apache.org/)
4. The following Python libraries:

		sudo pip3.6 install beautifulsoup4 colorzero gpiozero lxml netifaces parse password-strength pyppeteer pyquery requests requests-html selenium soupsieve urllib3 w3lib websockets
5. RouterSecc source code which can be downloaded from [github](https://github.com/mallisonNCSU/RouterSecc).

		git clone https://github.com/mallisonNCSU/RouterSecc
## Setup
+ After the above steps are completed, move / copy the contents in the directory to apache's hosting directory.

		sudo mkdir /var/www/html
		sudo cp RouterSecc/* /var/www/html
+ To run the python script on system startup, follow the tutorial from [this blog](https://blog.startingelectronics.com/auto-start-a-desktop-application-on-the-rapberry-pi/).

+ To setup static IP, follow this [forum post](https://www.raspberrypi.org/forums/viewtopic.php?t=191140).
	if you don't wish to setup a static IP, you will need to find your Raspberry Pi's IP address with ifconfig
+ To add the LED indication and reset push button to the Raspberry Pi, the wiring diagram is shown as below.
	
![wiring diagram](https://github.com/mallisonNCSU/RouterSecc/blob/master/HW_System_Wiring_Diagram.png)
## Running the program
If the steps above are followed and completed, the program will be running automatically upon startup of the Raspberry Pi! To perform the tests and get the test results, you simply need to:

+ Power up the Raspberry Pi.
+ Connect the Raspberry Pi to a router's LAN interface through an RJ45 Ethernet cable.
+ Connect your phone, tablet, or laptop to the router's WiFi, open the internet browser and go to the Raspberry Pi's IP address, where test progress as well as results are shown.
+ Press the reset button if you wish to rerun the test on another router.
## Note
+ If pyppeteer's Chromium does not install correctly, copy your already-installed chromium executable into the default pyppeteer install location (found [here](https://miyakogi.github.io/pyppeteer/reference.html)).
