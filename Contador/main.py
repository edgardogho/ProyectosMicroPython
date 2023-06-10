import tm1637
import machine
from machine import Pin
from time import sleep_us, sleep_ms
#Utilizo biblioteca tm1637.py
tm = tm1637.TM1637(clk=Pin(5), dio=Pin(16))

#Variable que lleva la cuenta
cuenta = 0

#LedAzul incluido en la placa (pin 2)
ledAzul = machine.Pin(2,Pin.OUT)

#Variables que llevan el estado de cada boton.
estadoCuentaMas = 0
estadoCuentaMenos = 0

#Pines de entrada con los botones
botonCuentaMenos = machine.Pin(12,Pin.IN,Pin.PULL_UP)
botonCuentaMas = machine.Pin(14,Pin.IN,Pin.PULL_UP)

#Cuando se enciende se pone en cero
tm.number(0)

#Loop infinito
while True:
    #Reflejar en el ledAzul el estado del boton de cuenta Mas
    ledAzul.value(botonCuentaMas.value())
    #Cuenta mas debe detectar 3 ms de 0 para pasar a sumar cuenta
    if estadoCuentaMas == 0 and not botonCuentaMas.value():
        sleep_ms(3)
        if not botonCuentaMas.value():
            #Cuenta uno y pasa a estado 1
            cuenta = cuenta + 1
            tm.number(cuenta)
            estadoCuentaMas = 1
    #Si estadoCuentaMas = 1 y boton en 1, vuelve a esperar
    if estadoCuentaMas == 1 and botonCuentaMas.value():
        estadoCuentaMas = 0
    
    #Misma logica para Cuenta Menos
    if estadoCuentaMenos == 0 and not botonCuentaMenos.value():
        sleep_ms(3)
        if not botonCuentaMenos.value():
            if cuenta>0:
                cuenta = cuenta - 1
            tm.number(cuenta)
            estadoCuentaMenos = 1
    if estadoCuentaMenos == 1 and botonCuentaMenos.value():
        estadoCuentaMenos = 0
