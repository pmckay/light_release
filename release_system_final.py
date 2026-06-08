from machine import I2C, SoftI2C, Pin
from time import sleep_ms, ticks_ms, ticks_diff
import urtc
import TSL2591


# the release system: controlling the instrument and supports data documenting
def release_system(): 

    # Define pins and sensors

    # Real Time Clock (DS3231)
    i2c_rtc = I2C(0, sda=(12), scl=(13), freq=400000)
    rtc = urtc.DS3231(i2c_rtc)

    # Light Sensor (TSL2591)
    i2c_light = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)
    light_sensor = TSL2591.TSL2591(i2c_light)
    # Set the gain to low 
    light_sensor.gain = TSL2591.GAIN_LOW

    relay = Pin(15, Pin.OUT)
    # defalt: not released 
    relay.value(0)
    
    start = ticks_ms()
    # duration = 60 * 60 * 1000 # 1 hour, modify if needed
    duration = 1000 * 60 * 15 # 15 minutes (for testing)
    min_lux = 2000
    max_lux = 10000
    measurements = open("measurements.csv", "a")
    measurements.write("datetime,lux,relay \n")
    measurements.flush()

    while ticks_diff(ticks_ms(), start) < duration:
        lux = light_sensor.lux
        if lux >= min_lux and lux < max_lux:
            relay.value(1)
            print(relay.value(), "released")
            sleep_ms(5000)
            relay.value(0)
            print("relay set to 0")
        else:
            relay.value(0)
            sleep_ms(5000)
            
        print("lux:", lux, "relay:", relay.value())
        documentToFile(rtc, measurements, lux, relay)
        sleep_ms(5000)

    minutes = ticks_diff(ticks_ms(), start) / (1000 * 60)
    print(f"The instrument has been deployed for {minutes:.2f} minute(s).")
    relay.value(1)
    sleep_ms(5000)
    documentToFile(rtc, measurements, lux, relay)
    relay.value(0)
    print("relay_value: ", relay.value())
#     while True:
#         documentToFile(rtc, measurements, lux, relay)
#         sleep_ms(10000)
    measurements.flush()
    measurements.close()



# A helper function that formats the text to be written into the data file
def documentToFile(rtc, fileName, lux, relay):
    now = rtc.datetime()
    timestamp = "{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(now[0], now[1], now[2], now[4], now[5], now[6])
    fileName.write(timestamp + "," + str(lux) + "," + str(relay.value()) + "\n")
#     measurements.flush()
