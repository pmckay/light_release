import release_system_final
from machine import Pin
from time import sleep

# define input pins
pin18 = Pin(18, Pin.OUT)
pin19 = Pin(19, Pin.IN)
pin20 = Pin(20, Pin.OUT)

pin18.value(0)
pin20.value(1)

led = Pin("LED", Pin.OUT)

if pin19.value() == 1:
    print("System started.")
    led.on()
    sleep(3)
    led.off()
    release_system_final.release_system()
else:
    print("Failed to start the system. ")
