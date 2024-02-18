# GateOpenStatus
## Secure Your Home with CCTV Integration: Monitor Your Main Gate Status
**Are you concerned about unauthorized access to your property or unexpected movement around your home?**  Integrating your existing CCTV cameras with your security system can offer a robust solution for monitoring and enhancing your home security.
### Here's how it can work:
+ Live Monitoring:

  + This enables you to keep an eye on things remotely, whether you're away from home or simply checking in for peace of mind.
 
+ Motion Detection:

  + Configure your cameras and Home Assistant to trigger alerts upon detecting motion within designated areas.
  + Receive instant notifications on your phone or other devices, allowing you to investigate potential security breaches promptly.
 
+ Automation:

  + Combine motion detection with smart home devices like lights or sirens to create automated responses.
  + For example, upon detecting motion at night, lights could automatically switch on, deterring potential intruders.
### Enhanced Gate Status Detection: 
This program aims to deliver exceptional accuracy in detecting the main gate's open and closed states, even under challenging conditions. It addresses scenarios where shadows or small animals crossing the camera's view might lead to misinterpretations. To achieve this, the program incorporates three additional switches, specifically designed to enhance the reliability of the gate status information. This innovative approach ensures you receive clear and dependable notifications about your gate's position, fostering greater peace of mind and security.
### Technical Implementation:
+ **OpenCV and Template Matching:** The program utilizes [OpenCV](https://github.com/opencv/opencv) with the [matchTemplate](https://docs.opencv.org/3.4/d4/dc6/tutorial_py_template_matching.html) function for gate status detection without relying on AI algorithms.
+ **Zone of Interest Masking:** To speed up processing, the program masks irrelevant areas of the image, focusing only on the "Zone of Interest" where the gate is located.
### Challenges:
The challenge I'm forcing is that my camera has two different modes, the day mode with changing light situations and of course we have the night vision infrared mode which give us a different picture.

<img src="https://github.com/Leftaf/GateOpenStatus/assets/2380560/881ee043-091a-47f6-87f3-e71deb33e1c7" width="384" height="216">
<img src="https://github.com/Leftaf/GateOpenStatus/assets/2380560/e9ead131-8bd1-41dc-a744-15911933eb40" width="384" height="216">
<img src="https://github.com/Leftaf/GateOpenStatus/assets/2380560/7cb979c2-397b-4b9c-84a6-1e340caebd2c" width="384" height="216">

### Sources of inspiration:
The project draws inspiration from several online resources:

+ [Detect open door with traincascade?](https://answers.opencv.org/question/56779/detect-open-door-with-traincascade/)
+ [Door-Detection](https://github.com/oflynned/Door-Detection)\n
+ [door_detect](https://github.com/twstokes/door_detect)\n
+ [Check if a physical door is opened or closed with OpenCV](https://stackoverflow.com/questions/11327835/check-if-a-physical-door-is-opened-or-closed-with-opencv)

### Tries which didn't work: 
I also tried the approach:

1. Raw image is first converted to grey scale.
2. The image is then blurred to remove noise which would otherwise interfere with the detection process.
3. A threshold is then applied to the image to reduce the number of shades of grey present and thus simplify the detection process.
4. The Canny edge detection algorithm is then applied to see the gate shape.

But as my gate is Black in a Black night with infrared this methde doesn't see anything.

### so here my best Solution: 
I tried many transformations für my images and the best result had been with Template Matching I think if your Gate has a beeter strukture than my plain Black gate than this will even imporve your result. To tune my results I have used following solutions.

+ Standard Deviation and Threshold Adjustment: The program analyzes a history of frames to calculate an average threshold, adapting to changing light conditions.
+ GATE_THRESHOLD_TOLERANCE: This parameter defines the acceptable difference between the template image and the live stream for detecting gate state changes.
+ GATE_THRESHOLD_CHANGE_DECREMENT: This value accounts for slow gate movements, adjusting the threshold sensitivity to avoid false positives.
+ GATE_THRESHOLD_SMOOTHING: This parameter determines the number of frames required for the gate status to change, mitigating temporary fluctuations caused by wind or small animals.

### Conclusion:
This project demonstrates a successful approach to gate status detection using template matching and various adjustments to handle challenging lighting conditions. While the effectiveness may vary depending on gate design and environment, the provided techniques offer a valuable starting point for further development and exploration.
