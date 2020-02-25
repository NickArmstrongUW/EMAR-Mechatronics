import time
import sys
import RPi.GPIO as GPIO
import rospy
import std_msgs.msg
DEBUG = 1

class FSR_Reader:
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
	def __init__(self, CLK, MISO, MOSI, CS, adcnum = 0):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(MOSI, GPIO.OUT)
		GPIO.setup(MISO, GPIO.IN)
		GPIO.setup(CLK, GPIO.OUT)
		GPIO.setup(CS, GPIO.OUT)
		self.clockpin = CLK
		self.mosipin = MOSI
		self.misopin = MISO
		self.cspin = CS
		self.adcnum = adcnum
                rospy.init_node('head and body node')


	def read(self):
		return self.readadc(self.clockpin, self.mosipin, self.misopin, self.cspin)

	def outputStream(self):
		while(True):
			print self.read()
		
	def readadc(self, clockpin, mosipin, misopin, cspin):

		if ((self.adcnum > 7) or (self.adcnum < 0)):
			return -1
		GPIO.output(cspin, True)
		GPIO.output(clockpin, False)  # start clock low
		GPIO.output(cspin, False)     # bring CS low

		commandout = self.adcnum
		commandout |= 0x18  # start bit + single-ended bit
		commandout <<= 3    # we only need to send 5 bits here
		for i in range(5):
			if (commandout & 0x80):
				GPIO.output(mosipin, True)
			else:
				GPIO.output(mosipin, False)
			commandout <<= 1
			GPIO.output(clockpin, True)
			GPIO.output(clockpin, False)

		adcout = 0
		# read in one empty bit, one null bit and 10 ADC bits
		for i in range(12):
			GPIO.output(clockpin, True)
			GPIO.output(clockpin, False)
			adcout <<= 1
			if (GPIO.input(misopin)):
				adcout |= 0x1

		GPIO.output(cspin, True)
		
		adcout >>= 1       # first bit is 'null' so drop it
		return adcout

	def format(self, val):
		return int(round(val / 10.24))

	def changeAdcnum(self, adcnum):
		self.adcnum = adcnum;
		



#Main for testing values

#!/usr/bin/env python
def fsrTest():
        head_pub = rospy.Publisher('Head_Haptics', std_msgs.msg.String, queue_size = 10)
        body_pub = rospy.Publisher('Body_Haptics', std_msgs.msg.String, queue_size = 10)
        vTol = 3
	fTol = 4
	r0 = FSR_Reader(18,23,24,25)
	r5 = FSR_Reader(18,23,24,25, 5);
	if len(sys.argv) > 1:
		audioFile = sys.argv[1]

	lastFDif = 0
	lastF = r0.format(r0.read())
	lastV = r5.format(r5.read())
	time.sleep(0.5)
	while(True):
		newF = r0.format(r0.read())
		newV = r5.format(r5.read())
		print "FSR: " + str(newF) + "%"
                body_pub.publish(str(newF))
		fDif = newF - lastF
		print "FSR Change: " + str(fDif)
		print "Velostat: " + str(newV)
                head_pub.publish(str(newV))
                vDif = newV - lastV
                print "Velostat Change: " + str(vDif)

		
		# sleep inbetween detections 
		# (doesn't need to be constantly detecting)
		time.sleep(.1)
		lastF = newF
		lastV = newV
		lastFDif = fDif

if __name__ == "__main__":
	fsrTest()




"""
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
potentiometer_adc = 0;

last_read = 0       # this keeps track of the last potentiometer value
last_read = 0       # this keeps track of the last potentiometer value
tolerance = 5       # to keep from being jittery we'll only change
					# volume when the pot has moved more than 5 'counts'

while True:
		# we'll assume that the pot didn't move
		trim_pot_changed = False

		# read the analog pin
		trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
		# how much has it changed since the last read?
		pot_adjust = abs(trim_pot - last_read)

		if DEBUG:
				print "trim_pot:", trim_pot
				print "pot_adjust:", pot_adjust
				print "last_read", last_read

		if ( pot_adjust > tolerance ):
			   trim_pot_changed = True

		if DEBUG:
				print "trim_pot_changed", trim_pot_changed

		if ( trim_pot_changed ):
				set_volume = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
				set_volume = round(set_volume)          # round out decimal value
				set_volume = int(set_volume)            # cast volume as integer

				print 'Volume = {volume}%' .format(volume = set_volume)
				set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
				os.system(set_vol_cmd)  # set volume

				if DEBUG:
						print "set_volume", set_volume
						print "tri_pot_changed", set_volume

				# save the potentiometer reading for the next loop
				last_read = trim_pot

		# hang out and do nothing for a half second
		time.sleep(0.5)
"""
