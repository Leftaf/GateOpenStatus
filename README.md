# GateOpenStatus
## Secure Your Home with CCTV Integration by check the status of your main gate
Are you concerned about unauthorized access to your property or unexpected movement around your home? Integrating your existing CCTV cameras in your security environment can offer a robust solution for monitoring and enhancing your home security.

+ Live Monitoring:

  + This enables you to keep an eye on things remotely, whether you're away from home or simply checking in for peace of mind.
 
+ Motion Detection:

  + Configure your cameras and Home Assistant to trigger alerts upon detecting motion within designated areas.
  + Receive instant notifications on your phone or other devices, allowing you to investigate potential security breaches promptly.
 
+ Automation:

  + Combine motion detection with smart home devices like lights or sirens to create automated responses.
  + For example, upon detecting motion at night, lights could automatically switch on, deterring potential intruders.
 
This program aims to deliver exceptional accuracy in detecting the main gate's open and closed states, even under challenging conditions. It addresses scenarios where shadows or small animals crossing the camera's view might lead to misinterpretations. To achieve this, the program incorporates three additional switches, specifically designed to enhance the reliability of the gate status information. This innovative approach ensures you receive clear and dependable notifications about your gate's position, fostering greater peace of mind and security.

In general I'm using [OpenCV](https://github.com/opencv/opencv) with [matchTemplate](https://docs.opencv.org/3.4/d4/dc6/tutorial_py_template_matching.html) without AI allgorithim and Mask Zone of Intressed to speedup the processing.

The challenge I'm forcing is that my camera has two different modes, the day mode with changing light situations and of course we have the night vision infrared mode which give us a different picture.

<img src="https://github.com/Leftaf/GateOpenStatus/assets/2380560/881ee043-091a-47f6-87f3-e71deb33e1c7" width="384" height="216">
<img src="https://github.com/Leftaf/GateOpenStatus/assets/2380560/e9ead131-8bd1-41dc-a744-15911933eb40" width="384" height="216">
<img src="https://github.com/Leftaf/GateOpenStatus/assets/2380560/7cb979c2-397b-4b9c-84a6-1e340caebd2c" width="384" height="216">

Thats why I have wrote this Programm with:

+ history of the last 200 frames of standard deviation adds the max Value to the tolerance
+ GATE_THRESHOLD_TOLERANCE: float = 0.03 this is the default between the original and live stream to detect open and close
+ GATE_THRESHOLD_CHANGE_DECREMENT: float = 0.0001 if the gate opens slowly the standard deviation my work to good thats why it could make sence to lower the value 
+ GATE_THRESHOLD_SMOOTHING = 20 sometimes due to wind or small animals cross the gate and here you can decide how many frames until the status will change.

As I also found only a few places where this Topic has been discribted I though to share my result. 

One Post from 2015 -> [Detect open door with traincascade?](https://answers.opencv.org/question/56779/detect-open-door-with-traincascade/) 
secound Post from 2016 -> [Door-Detection](https://github.com/oflynned/Door-Detection)
third Post from 2021 -> [door_detect](https://github.com/twstokes/door_detect)
fourth Post from 2012 -> [Check if a physical door is opened or closed with OpenCV](https://stackoverflow.com/questions/11327835/check-if-a-physical-door-is-opened-or-closed-with-opencv)
