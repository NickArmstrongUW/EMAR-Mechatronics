#!/usr/bin/env python
from emar_msg import WoZCommand
import rospy

def callback(data):
  #set neck to value
  print("Neck changing to position", str(data))
  #TODO: Impliment DynamixelSDK

def listeners():
  # currently just subbed to the Neck_Commands topic
  rospy.init_node("neck_listeners", anonymous=False)
  woz_sub = rospy.Subscriber('Neck_Commands', WoZCommand, callback)
  rospy.spin()



if __name__ == '__main__':
	try:
		listeners()
	except rospy.InterruptExption:
		pass
