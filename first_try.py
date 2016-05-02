##import RPi.GPIO as GPIO
import time
import json
##import requests
import urllib2
import datetime


def get_conditions(url):
    try:
        f = urllib2.urlopen(url)
    except:
        print "Failed to get conditions"
        return False
    json_conditions = f.read()
    f.close()
    return json.loads(json_conditions)
##Weather underground setup
api_key = 'df3d6145d5f21ac1'
base = 'http://api.wunderground.com/api/' + api_key
location1 = '/conditions/q/sweden/stockholm.json'
location2 = '/conditions/q/australia/sydney.json'
astronomy1 = '/astronomy/q/sweden/stockholm.json'
astronomy2 = '/astronomy/q/australia/sydney.json'
finalurl1 = base + location1
finalurl2 = base + location2
wakeupurl1 = base + astronomy1
wakeupurl2 = base + astronomy2
#board io setup
##GPIO.setmode(GPIO.BOARD)
led = 23
left_button = 22
right_button = 21
location = 1
##GPIO.setup(led, GPIO.OUT)
##GPIO.setup(right_button, GPIO.OUT)
##GPIO.setup(left_button, GPIO.OUT)
#other setup
conditions1 = get_conditions(finalurl1)
conditions2 = get_conditions(finalurl2)
start_time = datetime.datetime.now().time().hour
get_wake_time1 = get_conditions(wakeupurl1)
get_wake_time2 = get_conditions(wakeupurl2)
waketime1 = int(get_wake_time1['sun_phase']['sunrise']['hour'])
waketime2 = int(get_wake_time2['sun_phase']['sunrise']['hour'])
turnon = False
counter1 = 0
counter2 = 0
##now check you got the right api key
if ('current_observation' not in conditions1):
    print "Error! Wunderground API call failed"
    if 'error' in conditions1['response']:
        print "Error Type: " + conditions1['response']['error']['type']
        print "Error Description: " + conditions1['response']['error']['description']
    exit()
try:
    while True:
        ##while GPIO.input(left_button) and GPIO.input(right_button):
            ##pass
        ##if GPIO.input(left_button) == False:
            ##location = 1
        ##if GPIO.input(right_button) == False:
            ##location = 2
        #update
        looptime = int(datetime.datetime.now().time().hour)
        if looptime == waketime1 or ((looptime <= waketime1+2) and (looptime >= waketime1)):
            if counter1 > 100:
                conditions1 = get_conditions(finalurl1)
                counter1 = 0
            turnon = True
        if looptime == waketime2 or ((looptime <= waketime2+2) and (looptime >= waketime2)):
            if counter2 > 100:
                conditions2 == get_conditions(finalurl2)
                counter2 = 0
            turnon = True
        if looptime == 23:
            waketime1 = int(get_wake_time1['sun_phase']['sunrise']['hour'])
            waketime2 = int(get_wake_time2['sun_phase']['sunrise']['hour'])
            #update the wake time too
        #location changes change wind info used
        if location == 1:
            current_wind = conditions1['current_observation']['wind_kph']
        else:
            current_wind = conditions2['current_observation']['wind_kph']
        #debugging of wind info
        print counter1, counter2
        if(current_wind >= 10) and (turnon):
            print "placeholder"
            ##GPIO.output(led, 1)
        else:
            print "placeholder2"
            ##GPIO.output(led, 0)
        counter1 = counter1 + 1
        counter2 = counter2 + 1
        if counter1 > 200:
            counter1 = 0
        if counter2 > 200:
            counter2 = 0
        # still need to update wake up times
except KeyboardInterrupt:
    #GPIO.cleanup()
    exit()



