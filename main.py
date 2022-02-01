import time
import machine
import network
import esp
import micropython
import ubinascii
from umqttsimple import MQTTClient
import hcsr04
import ConnectWifi

ConnectWifi.connect()

client = MQTTClient("ESP32_001", "linuxaws.ddns.net", port=1883)
client.connect()
A_b = machine.Pin(4, machine.Pin.OUT)
A_g = machine.Pin(2, machine.Pin.OUT)
A_r = machine.Pin(15, machine.Pin.OUT)
B_b = machine.Pin(19, machine.Pin.OUT)
B_g = machine.Pin(18, machine.Pin.OUT)
B_r = machine.Pin(5, machine.Pin.OUT)
C_b = machine.Pin(23, machine.Pin.OUT)
C_g = machine.Pin(22, machine.Pin.OUT)
C_r = machine.Pin(21, machine.Pin.OUT)
while True:
    ultrasonic = hcsr04.HCSR04(trigger_pin=12, echo_pin=13)
    distance = ultrasonic.distance_cm()
    payload = distance
    print('Distance:', distance/0.1, 'MM', '|', distance, 'CM')
    if distance < 1:  #unzero timeout
        A_r.on()
        A_g.on()
        A_b.on()
        B_r.on()
        B_g.on()
        B_b.on()
        C_r.on()
        C_g.on()
        C_b.on()
        time.sleep(0.1)
    elif distance <= 20:
        A_r.on()
        A_g.on()
        A_b.on()
        B_r.on()
        B_g.on()
        B_b.on()
        C_r.on()
        C_g.off()
        C_b.on()
        client.publish("/TEST", "HELLO WORLD 123")
        time.sleep(0.1)
    elif distance > 21:
        A_r.on()
        A_g.on()
        A_b.on()
        B_r.on()
        B_g.on()
        B_b.on()
        C_r.on()
        C_g.on()
        C_b.on()
        time.sleep(0.1)
        
        
        
        
        
        
        
        
def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'Hello #%d' % counter
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()
    
