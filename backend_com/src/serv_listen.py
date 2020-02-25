#!/usr/bin/env python
import requests
import time
import json
import rospy
from std_msgs.msg import String
from msg import WoZCommand
from numpy import array_equal

def main():
	neck_pub = rospy.Publisher('Neck_Commands', WoZCommand, queue_size=10)
	led_pub = rospy.Publisher('LED_Commands', WoZCommand, queue_size=10)
	rospy.init_node("getServerCommands", anonymous=False)
	# Dummy data to represent the statius of the neck application
	# self.current_neck_pan = 0
	# self.current_neck_tilt = 0
	# self.tactile_data = {'sensor0':1, 'sensor1':1, 'sensor2':1};

	# Robot and database info
	current_neck_pan = 0
	current_neck_tilt = 0
	current_neck_pitch = 0
	current_rgb = [0, 0, 0]

	this_robot_id = 0
	URL = "https://emar-database.firebaseio.com/"
	AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyAisnI9BEW_Uc0-z1ad25nB6eNXEEQ_xQQ";
	headers = {'Content-type': 'application/json'}
	auth_params = {"returnSecureToken":"true"}

	# Start connection to Firebase and get anonymous authentication
	connection = requests.Session()
	connection.headers.update(headers)
	auth_request = connection.post(url=AUTH_URL, params=auth_params)
	auth_info = auth_request.json()
	auth_params = {'auth': auth_info["idToken"]}
	rate = rospy.Rate(10) # 10Hz
	while not rospy.is_shutdown():

		# Sending get request and obtaining the response
		get_request = connection.get(url = URL + "robots.json")
		# Extracting data in json format 
		robots = get_request.json()

		neck_action = robots[this_robot_id]["actions"]["neck"]
		led_action = robots[this_robot_id]["actions"]["led"]

		if (current_neck_pan != neck_action["panAngle"]):
			print("New neck pan value: " + str(neck_action["panAngle"]))
			current_neck_pan = neck_action["panAngle"]
			msg = WoZCommand()
			msg.name = "panAngle"
			msg.values[0] = neck_action["panAngle"]
			rospy.loginfo(msg)
			neck_pub.publish(msg)

		if (current_neck_tilt != neck_action["tiltAngle"]):
			print("New neck tilt value: " + str(neck_action["tiltAngle"]))
			current_neck_tilt = neck_action["tiltAngle"]
			msg = WoZCommand()
			msg.name = "tiltAngle"
			msg.values[0] = neck_action["tiltAngle"]
			rospy.loginfo(msg)
			neck_pub.publish(msg)

		# uncomment once WoZ is updated
		# if (current_neck_pitch != neck_action["pitchAngle"]):
		# 	print("New neck tilt value: " + str(neck_action["pitchAngle"]))
		# 	current_neck_tilt = neck_action["pitchAngle"]
		# 	msg = WoZCommand()
		# 	msg.name = "pitchAngle"
		# 	msg.values[0] = neck_action["pitchAngle"]
		# 	rospy.loginfo(msg)
		# 	neck_pub.publish(msg)
		
		# Woz Command not yet implimented
		# if not array_equal(current_rgb, led_action["rgb"]):
		# 	print("New RGB values: " + str(led_action["rgb"]))
		# 	current_rgb = led_action["rgb"]
		# 	msg = WoZCommand()
		# 	msg.name = "SetLedColor"
		# 	msg.values = led_action["rgb"]
		#	rospy.loginfo(msg)
		# 	led_pub.publish(msg)
			
		rate.sleep()

	#print(auth_info)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
	pass
