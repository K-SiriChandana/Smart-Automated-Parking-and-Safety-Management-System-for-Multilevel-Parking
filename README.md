# Smart-Automated-Parking-and-Safety-Management-System-for-Multilevel-Parking
Smart Parking System using Arduino: Designed and simulated in Tinkercad using IR sensors for slot detection, an ultrasonic sensor for vehicle entry detection,and a servo-controlled gate. Implemented RGB LED slot indicators and an I2C LCD display for real-time parking status,automated entry control.can use same code in arduino ide for real hardware 

## Features:

Real-time parking slot detection using IR sensors  
Ultrasonic sensor for vehicle detection at the entry gate  
Servo motor for automated gate control  
RGB LEDs indicating slot availability  
Green → Slot available  
Red → Slot occupied  
I2C LCD display showing number of free slots  
State machine logic for reliable gate operation  
Serial monitor logging for debugging  

## Hardware Components  
Arduino Uno  
IR sensors (4) – parking slot detection  
Ultrasonic sensor (HC-SR04) – vehicle detection  
Servo motor – gate control  
RGB LEDs (4) – slot indicators  
I2C 16x2 LCD display – parking status  
Resistors (used 700ohm)-for low current to passs so that RGB LEDs,arduino don't damage   
Breadboard and jumper wires

## Working Process  
The system works through the following process:  
IR sensors detect whether a car is present in each parking slot.  
Arduino reads sensor inputs and calculates available slots.  
RGB LEDs update the slot status.  
LCD displays the number of free parking spaces.  
When a vehicle approaches the entry gate (detected by ultrasonic sensor):  
If slots are available → gate opens.  
If parking is full → gate remains closed.  

## Pin Configuration
Component:      	Arduino Pin  
IR Sensor Slot 1:	2  
IR Sensor Slot 2:	3   
IR Sensor Slot 3:	4  
IR Sensor Slot 4:	5  
Servo Motor      :6  
RGB LED Slot 1	:7, 8  
RGB LED Slot 2	:11, 12  
RGB LED Slot 3	:13, A0  
RGB LED Slot 4	:A1, A2  
Ultrasonic TRIG :9  
Ultrasonic ECHO	:10  
LCD SDA          :	A4  
LCD SCL          :	A5  
