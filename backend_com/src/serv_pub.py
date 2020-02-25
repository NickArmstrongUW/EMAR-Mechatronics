#!/usr/bin/env python
import requests
import time
import json
import rospy
from std_msgs.msg import float32
from std_msgs.msg import hapticMsg




def main(** args):
	# Dummy data to represent the statius of the neck application
	self.current_neck_pan = 0
	self.current_neck_tilt = 0
	self.tactile_data = {'head0':0.0, 'headTouched':False, 'body0':0.0, 'bodyTouched':False}

	# Robot and database info
	self.this_robot_id = 0
	self.URL = "https://emar-database.firebaseio.com/"
	self.AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyAisnI9BEW_Uc0-z1ad25nB6eNXEEQ_xQQ";
	self.headers = {'Content-type': 'application/json'}
	self.auth_params = {"returnSecureToken":"true"}

	# Start connection to Firebase and get anonymous authentication
	self.connection = requests.Session()
	self.connection.headers.update(self.headers)
	self.auth_request = self.connection.post(url=self.AUTH_URL, params=self.auth_params)
	self.auth_info = self.auth_request.json()
	self.auth_params = {'auth': self.auth_info["idToken"]}
	rospy.init_node('hapticListener', anonymous=True)
	rospy.Subscriber('head_haptic_topic', hapticMsg, updateHeadData)
	rospy.Subscriber('body_haptic_topic', hapticMsg, updateBodyData)
	rospy.spin()

	#print(auth_info)

# listeners for the data from each sensor
# excpects data as a hapticMsg type
def sensorListener():
	

def send(data, tactile_data, this_robot_id): #TODO
	print "sending to server: " + str(data)
	tactile_data_json =  json.dumps(self.tactile_data)
	tactile_url = self.URL + "robots/" + str(self.this_robot_id) + "/inputs/tactile.json"
	post_request = self.connection.put(url=tactile_url,
		data=tactile_data_json, params=self.auth_params)
	
	print("Tactile sensor data sent: " + str(post_request.ok))
	return True

def updateHeadData(self, data): 
	self.tactile_data["head0"] = data.data[0]
	self.tactile_data["headTouched"] = data.isTouched
	send(data)

def updateBodyData(self, data):
	self.tactile_data["body0"] = data.data[0]
	self.tactile_data["bodyTouched"] = data.isTouched
	send(data)


	#########========


if __name__ == '__main__':
	main()
	try:
		getServerCommand()
	except rospy.InterruptExption:
		pass