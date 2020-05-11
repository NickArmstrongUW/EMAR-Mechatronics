cmake_minimum_required(VERSION 2.8.3)
project(emar_msg)

find_package(catkin REQUIRED COMPONENTS 
  rospy
  std_msgs
  message_generation)

add_message_files(
  FILES
  hapticMsg.msg
  WoZCommand.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS 
  message_runtime
  std_msgs
)

install(DIRECTORY include/std_msgs/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  PATTERN "*.h")
