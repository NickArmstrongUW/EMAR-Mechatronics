cmake_minimum_required(VERSION 2.8.3)
project(std_msgs)

find_package(catkin REQUIRED COMPONENTS message_generation)

add_message_files(
  hapticMsg
  WoZCommand
)

generate_messages()

catkin_package(
  INCLUDE_DIRS include
  CATKIN_DEPENDS message_runtime)

install(DIRECTORY include/std_msgs/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  PATTERN "*.h")
