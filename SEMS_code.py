#Setting pin names and board values based on RaspberryPi configuration
relay = 21 #output to light and fan 
room = 23 #motion sensor
flame = 5 #flame sensor
buzzer = 24 #buzzer for alaarm
green = 19
red = 16

#import libraries for inout and output from sensors, time and RFID module
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

#Clear any anamoly readings as False and declare kind of set up of board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
scan = SimpleMFRC522()

#Set pins as input and output accordingly
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(room, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(flame, GPIO.IN)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

while True:
	GPIO.output(relay, GPIO.HIGH) #switch relay off

	#fire alarm checking
	fire=GPIO.input(flame)
	if fire == GPIO.HIGH: 
		GPIO.output(buzzer, GPIO.LOW)
	else:
		GPIO.output(buzzer, GPIO.HIGH)

	#Scanning of RFID tag and check to see whether authorised
	print(“Place your card - “)
	id, Tag=scan.read()
	print(id)
	pre_set=“166061473145” #authorised value already configured 
	if str(id)!=pre_set: #entry denied
		GPIO.output(green,GPIO.LOW)
		GPIO.output(red,GPIO.HIGH)
		time.sleep(2)
		GPIO.output(red,GPIO.LOW)
		continue
	elif str(id)==pre_set: #entry allowed 
		GPIO.output(green,GPIO.HIGH)
		GPIO.output(red,GPIO.LOW)
		time.sleep()
		GPIO.output(green,GPIO.LOW)

		#loop to detect for motion once room is entered by authorised person
		while True:
			motion = GPIO.input(room)
			fire = GPIO.input(flame)
			if motion == GPIO.HIGH:
				print(“Motion detected.”)
				GPIO.output(relay, GPIO.LOW) #switches on
				if fire == GPIO.HIGH:
					GPIO.output(buzzer, GPIO.LOW)
				else:
					GPIO.output(buzzer, GPIO.HIGH)
			elif motion == GPIO.LOW:
				print(“No motion.”)
				GPIO.output(relay, GPIO.HIGH)  #switches off
				if fire == GPIO.HIGH:
					GPIO.output(buzzer, GPIO.LOW)
				else:
					GPIO.output(buzzer, GPIO.HIGH)

		

	
	
