# Net_monitor

Designed for WIZnet WS5100S-EVB-Pico contest.

https://maker.wiznet.io/2022/01/21/internet-outage-monitor/?success=1&post_id=25762

****** Network/internet outage monitor using WIZnet WS5100S-EVB-Pico ******

This project uses a WIZnet WS5100S-EVB-Pico attached to a spare Ethernet port on a local router. The Pico is used to monitor the Internet/Network connection for outages. 

The project was designed after chasing and tracking multiple home Internet outages.  


The program will:

•	Detect the Ethernet cable unplugged from the Pico or the Ethernet port

•	Detect Network or Internet outages

•	Light LEDs to indicate connection ok, cable disconnected and Network/Internet outages

•	Display tracking information through the serial port

•	Publish program start time, up time and outage time MQTT messages to a broker

   o	I used a Raspberry Pi as the broker and Node Red to post the information and write to a log 


Design:

•	The program is written in CircuitPython. Thronny is used as the editor.

•	Program file name is code.py. This allows the program to autostart on powerup. Note – the program will fail to start if the Ethernet cable is not plugged in.

•	The program will try to resolve a .com URL. I used dns.google. I also tested with my router URL.

•	The board and external green LEDs will be on during good connections.

•	If the program can’t resolve the URL, the external green LED will turn off and the red external LED will turn on.

•	If the Ethernet cable becomes unplugged, both the external and internal green LEDs will turn off and the external red LED will turn on.

•	The program will check the URL every 2 minutes and if there is an outage, it will check every 30 seconds.

•	All information will be displayed on the serial port.

•	Program start time, up time and outage time MQTT messages will be published to a broker. Note – outage time can not be sent until the network is back up.

   o	Optional – logging of program start time, up time and outage time.


Operating Modes

Normal operation:

![Normal operation](https://user-images.githubusercontent.com/13513067/164152993-e3de5b03-2e99-4964-8fc8-1f7138fec52e.jpg)

Ethernet cable disconnected:

![Cable disconnected](https://user-images.githubusercontent.com/13513067/164153130-e0c81613-63fe-4434-8425-0e4acb147726.jpg)

Network issue:

![Network issue](https://user-images.githubusercontent.com/13513067/164153191-cde6b16f-ee63-4a0d-8c0c-69a46836d010.jpg)


Node Red

![Screenshot 2022-04-13 160343](https://user-images.githubusercontent.com/13513067/163702247-930bede1-c342-48f8-8e98-a04671a1976e.jpg)
