# Robotics  
MAC address: 80:1f:02: ab:a6:24  
IP address can be found at:https://www.doc.ic.ac.uk/~ajd/robotics/index.cgi  
## Week 2  
For week 2 lab, we have tasks:  
- [x] Show us a Built and Working Pi/BrickPi Robot with Working WiFi and Motors (4 Marks)  
- [x] Controller Tuning (8 Marks)  
- [x] Distance and Rotation Calibration (5 Marks)  
- [x] Driving Accurately in a Square and Observing Drift (9 Marks)  
- [x] Calculating a Covariance Matrix (4 Marks)  
### Code Refactoring
To improve code readability and reduce complexity. The example code has been refactored. First, it is miscellaneous if we want to add left or right motor's parameter but copy this code block:![enter image description here](https://i.loli.net/2018/10/20/5bcb4d5891a8d.png){:height="30%" width="30%"}
What we did is to build a "json" file which contains all the parameter information in and everytime read from this "json" file.
### Controller Tuning  
We can use "Ziegler-Nichols" heuristic method to tune the PID parameter.</br>  
• set k<sub>i</sub>and k<sub>d</sub> to zero. Increase k<sub>p</sub> until the system starts oscillating with period P<sub>u</sub> (in seconds)  
— remember this gain as k<sub>u</sub>;</br>  
• set k<sub>p</sub> = 0.6k<sub>u</sub>, k<sub>i</sub> = 2k<sub>p</sub>/P<sub>u</sub>, and k<sub>d</sub> = k<sub>p</sub>P<sub>u</sub>/8.</br>  

## Week 3
- [ ] Simple On/Off Forward/Backward Control with Touch Sensors
- [ ] Forward/Backward Proportional Servoing with the Sonar Sensor
- [ ] Wall Following

## Week 4 questions

In theory the minimum range should be 0cm and the maximum range is 254cm. After observation, we found that 255 means 
it cannot detect the distance or something goes wrong. It always happens when we put the surface too close to the sensor 
camera. And in reality, our sensor has minimum range about 7cm and it will detect mistake error when the distance 
smaller than 3cm.