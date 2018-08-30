import RPi.GPIO as GPIO
import json
from azure.servicebus import ServiceBusService
import sys
import datetime
       
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)

failedBuilds = []

status = ""

if sys.argv[1] != "off":
    try:
        while True:
            bus_service = ServiceBusService(
                service_namespace='',
                shared_access_key_name='',
                shared_access_key_value='')
            
            msg = bus_service.receive_queue_message('buildFailures', peek_lock=True)
            
            if msg.body != None:
                jsonString = json.loads(msg.body.decode("utf-8"))
                status = jsonString["resource"]["status"]
                defID = jsonString["resource"]["definition"]["id"]
                defName = jsonString["resource"]["definition"]["name"]
                print("==============================")
                print("Definition Name: " + defName)
                print("Definition ID: " + str(defID))
                print("Status: " + status)
                if len(failedBuilds) > 0:
                    for build in failedBuilds:
                        if build == defID:
                            failedBuilds.remove(build)
                if status == "failed":
                    failedBuilds.append(defID)
            
            if status == "succeeded" and len(failedBuilds) == 0:
                print("LED green")
                print(str(datetime.datetime.now()))
                print("==============================")
                GPIO.output(17,GPIO.LOW)
                GPIO.output(18,GPIO.HIGH)
            elif status == "failed" or len(failedBuilds) > 0:
                print("LED red")
                print("Failed Build IDs:")
                print(", ".join(map(str,failedBuilds)))
                print(str(datetime.datetime.now()))
                print("==============================")
                GPIO.output(18,GPIO.LOW)
                GPIO.output(17,GPIO.HIGH)
               
            if msg.body != None:
                msg.delete()
                
    except KeyboardInterrupt:
        pass
    
else:
    GPIO.output(18,GPIO.LOW)
    GPIO.output(17,GPIO.LOW)    
