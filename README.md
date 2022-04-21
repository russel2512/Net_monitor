# Net_monitor

Designed for WIZnet WS5100S-EVB-Pico contest.

https://maker.wiznet.io/2022/01/21/internet-outage-monitor/?success=1&post_id=25762

**Network/internet outage monitor using WIZnet WS5100S-EVB-Pico**

This project uses a WIZnet WS5100S-EVB-Pico attached to a spare Ethernet port on a local router. The Pico is used to monitor the Internet/Network connection for outages. 

The project was designed after chasing and tracking multiple home Internet outages.  


**The program will:**

- Detect the Ethernet cable unplugged from the Pico or the Ethernet port

- Detect Network or Internet outages

- Light LEDs to indicate connection ok, cable disconnected and Network/Internet outages

- Display tracking information through the serial port

- Publish program start time, up time and outage time MQTT messages to a broker

  - I used a Raspberry Pi as the broker and Node Red to post the information and write to a log 


**Design:**
- The program is written in CircuitPython. Thronny is used as the editor.

- Program file name is code.py. This allows the program to autostart on powerup. Note – the program will fail to start if the Ethernet cable is not plugged in.

- The program will try to resolve a .com URL. I used dns.google. I also tested with my router URL.

- The board and external green LEDs will be on during good connections.

- If the program can’t resolve the URL, the external green LED will turn off and the red external LED will turn on.

- If the Ethernet cable becomes unplugged, both the external and internal green LEDs will turn off and the external red LED will turn on.

- The program will check the URL every 2 minutes and if there is an outage, it will check every 30 seconds.

- All information will be displayed on the serial port.

- Program start time, up time and outage time MQTT messages will be published to a broker. Note – outage time can not be sent until the network is back up.

  - Optional – logging of program start time, up time and outage time.



**Normal operation:**

![Serial port -1](https://user-images.githubusercontent.com/13513067/164374059-c697ab57-2236-4d6c-88a4-2cc02c4e4b33.jpg)

![Normal operation](https://user-images.githubusercontent.com/13513067/164152993-e3de5b03-2e99-4964-8fc8-1f7138fec52e.jpg)

**Ethernet cable disconnected:**

![Serial port - 2](https://user-images.githubusercontent.com/13513067/164374786-9ac5ba63-d854-4d15-9d8a-aa1767f951eb.jpg)

![Cable disconnected](https://user-images.githubusercontent.com/13513067/164153130-e0c81613-63fe-4434-8425-0e4acb147726.jpg)

**Network issue:**

![Network issue](https://user-images.githubusercontent.com/13513067/164153191-cde6b16f-ee63-4a0d-8c0c-69a46836d010.jpg)


**Node Red screen**

**Startup**
![Node Res - Start](https://user-images.githubusercontent.com/13513067/164322109-1e07b24e-673f-4efc-bfd3-1f850cb42d0b.jpg)

**Cable error**
![Node Red - Error](https://user-images.githubusercontent.com/13513067/164322256-e4e98656-07a6-48fe-b4a3-0dadf79e46de.jpg)

**Network error**
![Node Red - Network error](https://user-images.githubusercontent.com/13513067/164326331-28622515-88e5-42c9-9d5f-08bc062cb3c7.jpg)


