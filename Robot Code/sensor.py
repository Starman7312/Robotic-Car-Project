## Imports libraries
from gpiozero import DistanceSensor
import time

## Sets the pins to be used for operating the distance sensor
pintrigger = 17
pinecho = 18

## Instantiates the sensor object
sensor = DistanceSensor(echo = pinecho, trigger = pintrigger, max_distance = 50)

## Returns the distance measured by the sensor
def distance():
    d = sensor.distance
    return d

## Returns if an object is in contact with the sensor
def value():
    d = sensor.value
    return d
