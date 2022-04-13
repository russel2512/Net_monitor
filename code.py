"""
Developed by Russ Terrell
Written in Adafruit CircuitPython 7.1.1 on 2022-01-14; Raspberry Pi Pico with rp2040
Libraries developed by Adafruit and WIZnet

Version 1.00 04-00-2022

"""

import board
import busio
import digitalio
import rtc

from adafruit_datetime import datetime, date, time
from adafruit_wiznet5k.adafruit_wiznet5k_ntp import NTP
from adafruit_wiznet5k.adafruit_wiznet5k import *
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import adafruit_wiznet5k.adafruit_wiznet5k_dns as dns
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# SPI0
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17
# reset
W5x00_RSTn = board.GP20
ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT
# spi_bus
cs = digitalio.DigitalInOut(SPI0_CSn)
spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

# Onboard LED
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
# External Green - Connection good
led_og = digitalio.DigitalInOut(board.GP14)
led_og.direction = digitalio.Direction.OUTPUT
# External Red - Connection error
led_or = digitalio.DigitalInOut(board.GP15)
led_or.direction = digitalio.Direction.OUTPUT

# Note - IP network addresses may be different
# Setup your network configuration below
# Change IP address to an open address
IP_ADDRESS = (192, 168, 68, 200)
SUBNET_MASK = (255, 255, 255, 0)
GATEWAY_ADDRESS = (192, 168, 68, 1)
DNS_SERVER = (8, 8, 8, 8)

ntp_server_port= 123
NTP_URL = "time.google.com"

# URL to test. Can be internal or external.
Test_URL = "dns.google"
#Test_URL = "tplinkdeco.net"

# MQTT publish Topics
mqtt_start = 'WIZnet/start'
mqtt_up = 'WIZnet/up'
mqtt_down = 'WIZnet/down'

# Reset W5500 first
ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

# --->> will not continue if ethernet cable is not connected
# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs)

led.value = True
led_og.value = True
led_or.value = False
net_up = False
down=""

# Set network configuration
eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)
ntpserver_ip = eth.pretty_ip(eth.get_host_by_name(NTP_URL))

mqtt_client = MQTT.MQTT(
    #setup your broker IP address
    broker="192.168.68.107",
    # change to secure mqtt connection
    username="rpi-pico",       
    password="wiznet",      
    is_ssl=False,
    socket_pool=None,
    ssl_context=None,
    keep_alive=60,
)

print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("IP address:", eth.pretty_ip(eth.ip_address))
print("NTP: %s" % ntpserver_ip)  
ntp = NTP(iface = eth, ntp_address = ntpserver_ip ,utc = -5)
#Change utc value for time zone

#set Real Time Clock
cal = ntp.get_time()
r = rtc.RTC()
r.datetime = time.struct_time((cal.tm_year, cal.tm_mon, cal.tm_mday, cal.tm_hour, cal.tm_min, 00, 0, -1, -1))
dt = datetime.now()
print("Starting monitor", dt)
start="Start,"+str(dt.time())+","+str(dt.date())

# Initialize MQTT interface with the ethernet interface
MQTT.set_socket(socket, eth)

# Update Start time/date
mqtt_client.connect()
mqtt_client.publish(mqtt_start, start)
print("{0} topic send {1} to broker".format(mqtt_start, start))
time.sleep(1)
mqtt_client.disconnect()

# Clear Down
print(">>> Clear Down info")
mqtt_client.connect()
mqtt_client.publish(mqtt_down, down)
print("{0} topic send {1} to broker".format(mqtt_down, down))
time.sleep(1)
mqtt_client.disconnect()

# log first Up time/date
print(">>> First pass")
dt = datetime.now()
print("Up ",dt)
up="Up,"+str(dt.time())+","+str(dt.date())
mqtt_client.connect()
mqtt_client.publish(mqtt_up, up)
print("{0} topic send {1} to broker".format(mqtt_up, up))
time.sleep(1)
mqtt_client.disconnect()
net_up = True
    
def main():
    global net_up
    print("Test",Test_URL, "-->> %s" % eth.pretty_ip(eth.get_host_by_name(Test_URL)), datetime.now())
    if net_up == False:
        mqtt_client.connect()
        mqtt_client.publish(mqtt_down, down)
        print("{0} topic send {1} to broker".format(mqtt_down, down))
        time.sleep(1)
        mqtt_client.disconnect()

        dt = datetime.now()
        print("Up ",dt)
        up="Up,"+str(dt.time())+","+str(dt.date())
        mqtt_client.connect()
        mqtt_client.publish(mqtt_up, up)
        print("{0} topic send {1} to broker".format(mqtt_up, up))
        time.sleep(1)
        mqtt_client.disconnect()

    led.value = True
    led_og.value = True
    led_or.value = False
    net_up = True
while True:
    try:
        main()        
        time.sleep(120)
    except Exception as e:
        if net_up == True:
            dt = datetime.now()
            print("Down ",str(e),dt)
            down="Down,"+str(e)+","+str(dt.time())+","+str(dt.date())
            led_og.value = False
            led_or.value = True
            net_up = False
            # led.value = False if cable is disconnected
            if e.args == ('Ethernet cable disconnected!',):
                led.value = False
            time.sleep(30)
            # led.value = True if network or Internet is down

#finish
led.value = False
led_og.value = False
led_or.value = False

