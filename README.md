# WIZnet_monitor

Designed for WIZnet WS5100S-EVB-Pico contest.

https://maker.wiznet.io/2022/01/21/internet-outage-monitor/?success=1&post_id=25762

**Network/internet outage monitor using WIZnet WS5100S-EVB-Pico**

This project uses a WIZnet WS5100S-EVB-Pico attached to a spare Ethernet port on a local router. The WS5100S is used to monitor the Internet/Network connection for outages. The project was designed after chasing and tracking multiple home Internet outages.  



**The program will:**

- Detect the Ethernet cable unplugged from the WS5100S or the Ethernet port on the router
- Detect Network or Internet outages
- Light LEDs to indicate connection ok, cable disconnected and Network/Internet outages
- Display tracking information through the serial port
- Publish program start time, up time and outage time MQTT messages to a broker
  - I used a Raspberry Pi as the broker and Node Red to post the information and write to a log 



**Design:**

- The program is written in CircuitPython. Thronny is used as the editor.
- Program file name is code.py. This allows the program to autostart on powerup. **Note –** *the program will fail to start if the Ethernet cable is not plugged in.*
- The program will try to resolve a **.com** URL. I used **dns.google**. The program was also tested with my router URL.
- The board and external green LEDs will be on during good connections.
- If the program can’t resolve the URL, the external green LED will turn off and the red external LED will turn on.
- If the Ethernet cable becomes unplugged, both the external and internal green LEDs will turn off and the external red LED will turn on.
- The program will check the URL every 2 minutes and if there is an outage, it will check every 30 seconds to determine if the outage has cleared.
- All information will be displayed on the serial port.
- Program start time, up time and outage time will be published as MQTT messages to a broker. **Note –** *outage time can not be sent until the network is back up.*
- Use a Raspberry Pi for the MQTT broker. Use Node Red for data presentation and logging of program start time, up time and outage time. **Note –** *a broker must be available to the program to publish MQTT messages. If one isn't available, remark all publish calls in the program.*


**Circuit diagram**

![circuit](https://user-images.githubusercontent.com/13513067/164536405-280b8052-20c9-4218-bf58-c11763f9d29a.jpg)


**Deployment:**

This is an overview of the project deployment. You should have a general knowledge of RP2040. Information can be found at https://www.raspberrypi.com/products/raspberry-pi-pico/ and https://docs.wiznet.io/Product/iEthernet/W5100S/w5100s-evb-pico/. 

This project was developed with CircuitPython 7.1.1 deployed on the WS5100S. A good reference can be found at https://learn.adafruit.com/welcome-to-circuitpython.   
Version 7.1.1 of CircuitPython (adafruit-circuitpython-raspberry_pi_pico-en_US-7.1.1.uf2) can be found here:
https://adafruit-circuit-python.s3.amazonaws.com/bin/raspberry_pi_pico/en_US/adafruit-circuitpython-raspberry_pi_pico-en_US-7.1.1.uf2

Install Thonny IDE to program the WS5100S. It can be found here: https://thonny.org/.
**MU does not need to be installed.**

Create **lib** folder on the board.

Test CircuitPython with the WS5100S using the Blink example program.

After the testimg with Blink, download and copy the following libraries from:

https://github.com/Wiznet/RP2040-HAT-CircuitPython 

- adafruit_bus_device
- adafruit_io
- adafruit_minimqtt
- adafruit_wiznet5k
- adafruit_wsgi
- adafruit_requests.py

You will need to copy one more library to the lib folder:
Libraries (circuitpython.org)
adafruit-circuitpython-bundle-7.x-mpy-20220413.zip
Upzip the file and copy adafruit_datetime.mpy

Copy the monitor code:
russel2512/Net_monitor (github.com) 
code.py (autorun)
https://github.com/russel2512/Net_monitor/blob/main/code.py
WIZnet_monitor.py (same as code.py, but does not autorun)
https://github.com/russel2512/Net_monitor/blob/main/WIZnet_monitor.py

Connect the LEDs per the circuit diagram found in the GitHub project.

I'm not going into the details on how to setup a Raspberry Pi. 
For information on Raspberry Pi deployment, see Raspberry Pi.
For information on Mosquitto MQTT broker, see Install Mosquitto Broker Raspberry Pi | Random Nerd Tutorials.
For information on Node Red, see Running on Raspberry Pi : Node-RED (nodered.org).
- Change the MQTT ip adress to the broker.
- Change IP_ADDRESS if the device is on a different subnet or if 192.168.68.200 conflicts with device on your network.

For the program to work correctly a MQTT broker must be available or it will fail. A broker can be deployed on almost any device. If you don't have a broker available, you can go through the code and remark out all the MQTT calls.


**Serial Port display inforamtion with screen shots of LED status:**

**Normal operation:**

![Serial port -1](https://user-images.githubusercontent.com/13513067/164374059-c697ab57-2236-4d6c-88a4-2cc02c4e4b33.jpg)

![Normal operation](https://user-images.githubusercontent.com/13513067/164152993-e3de5b03-2e99-4964-8fc8-1f7138fec52e.jpg)

**Ethernet cable disconnected:**

![Serial port - 2](https://user-images.githubusercontent.com/13513067/164374786-9ac5ba63-d854-4d15-9d8a-aa1767f951eb.jpg)

![Cable disconnected](https://user-images.githubusercontent.com/13513067/164153130-e0c81613-63fe-4434-8425-0e4acb147726.jpg)

**Network issue:**

![Serial port - 3](https://user-images.githubusercontent.com/13513067/164514162-cff9395a-c566-405b-92af-02572847e671.jpg)

![Network issue](https://user-images.githubusercontent.com/13513067/164153191-cde6b16f-ee63-4a0d-8c0c-69a46836d010.jpg)


**Node Red screen shots**

**Startup**
![Node Res - Start](https://user-images.githubusercontent.com/13513067/164322109-1e07b24e-673f-4efc-bfd3-1f850cb42d0b.jpg)

**Cable error**
![Node Red - Error](https://user-images.githubusercontent.com/13513067/164322256-e4e98656-07a6-48fe-b4a3-0dadf79e46de.jpg)

**Network error**
![Node Red - Network error](https://user-images.githubusercontent.com/13513067/164326331-28622515-88e5-42c9-9d5f-08bc062cb3c7.jpg)


**Future enhancements:**

These are just ‘blue sky’ ideas. Some may not be valid or work. The biggest ‘got ya’ is the fact that the down/up information can’t be sent to the broker until the network is backup. This means the data will always cause a notification after the outage.

- Break up data for better data handling (ie, filling JASON fields and adding to databases)
- Deploy MQTT broker on PC and or Phone
- Use IFFT to send phone or text notifications
- Calculate downtime in the program or in Node Red
- Send Start, Up and Down data to external collection (ie ThingSpeak)
- Send notifications to a phone or PC directly from Node Red
- Add code to monitor multiple URLs, this could be used to monitor multiple servers or internal network devices (must have URLs)

