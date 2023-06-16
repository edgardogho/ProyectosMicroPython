import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import dht
import json
from machine import Pin

esp.osdebug(None)
import gc
gc.collect()

sensor = dht.DHT22(Pin(2))

ssid = 'ssid'
password = 'clave'
#mqtt_server = 'io.adafruit.com'

mqtt_server = 'serverip'
port = 8741
client_id = 'grupo6_2'
topic_sub = 'grupo6/topic_pub'
topic_pub = 'grupo6/topic_sub'
#topic2_pub = b'edgardogho/feeds/temperatura'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


def sub_cb(topic, msg):
  print((topic, msg))
  dato = msg.decode('utf-8')
  topicrec = topic.decode('utf-8')
  if topicrec == topic_sub and "OFF" in dato and "led" in dato:
    pin = machine.Pin(3, machine.Pin.OUT)
    pin.value(0)
    print('LED APAGADO')
  else:
    pin = machine.Pin(3, machine.Pin.OUT)
    pin.value(1)
    print('LED PRENDIDO')  

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server,user='alumnos',password='alumnos',port=int(port))
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
    time.sleep(1)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    #adc = machine.ADC(0)
    #mensaje = b'%d' %adc.read()
    cadenatemp = {"tipo":"temperatura","valor":str(temp)}
    datos = json.dumps(cadenatemp)
    client.publish(topic_pub,datos)
    cadenahum = {"tipo":"humedad","valor":str(hum)}
    datos = json.dumps(cadenahum)
    client.publish(topic_pub,datos)
    #client.publish(topic2_pub,str(temp))
  except OSError as e:
    restart_and_reconnect()
