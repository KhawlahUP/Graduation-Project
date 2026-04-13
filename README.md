# Smart Glasses Remote Control (SGRC) 👓✨

![SGRC](https://github.com/user-attachments/assets/a12ee6f2-d39f-426e-a3f7-d9a77aa35d9d)

## Overview
Smart Glasses Remote Control (SGRC) is an innovative wearable system that allows users to control IoT devices using hand and head gestures captured by smart glasses. Utilizing AI technologies like gesture recognition and object detection, the system enables touch-free interaction with smart home appliances.

> **Built with:** Python, MediaPipe, OpenCV, Raspberry Pi, ESP8266 (NodeMCU), MQTT

---

## 📁 Repository Structure
Based on the project architecture, the files are organized as follows:
* **`/Diagram`**: Engineering schematics, block diagrams, and system concept designs.
* **`/Hand Gesture Control`**: Real-time testing results showing the system controlling various devices.
* **`/Hardware 3D`**: STL files for 3D printing (Gears, Brackets, and Sensor mounts).
* **`/Simulation`**: Proteus project files and required libraries for virtual testing.
* **`/Software`**: Source code including Python scripts for Raspberry Pi and C++ for NodeMCU.

---

## 📐 System Architecture
```mermaid
graph TD
    User[👤 User] -->|🖐️ Gestures| Camera[📷 Camera]
    Camera -->|🎥 Video Feed| RaspberryPi[🍓 Raspberry Pi]
    RaspberryPi -->|📡 MQTT| ESP8266[📶 ESP8266]
    ESP8266 -->|🔌 Control| IoT_Devices[🏠 IoT Devices]
🧩 Hardware Components
<table>
<tr>
<th>Image</th>
<th>Component</th>
<th>Description</th>
</tr>
<tr>
<td align="center"><img src="images/nodemcu.jpg" width="80"/></td>
<td><strong>NodeMCU V3</strong></td>
<td>ESP8266 microcontroller for wireless IoT control.</td>
</tr>
<tr>
<td align="center"><img src="images/relay.jpg" width="80"/></td>
<td><strong>Relay</strong></td>
<td>Electronic switch for high-voltage devices like fans.</td>
</tr>
<tr>
<td align="center"><img src="images/led.jpg" width="80"/></td>
<td><strong>LED</strong></td>
<td>Visual indicator for system feedback and status.</td>
</tr>
<tr>
<td align="center"><img src="images/fan.jpg" width="80"/></td>
<td><strong>Mini Fan</strong></td>
<td>5V DC fan controlled via gesture commands.</td>
</tr>
<tr>
<td align="center"><img src="images/raspberrypi.jpg" width="80"/></td>
<td><strong>Raspberry Pi</strong></td>
<td>Central processing unit for AI and gesture recognition.</td>
</tr>
<tr>
<td align="center"><img src="images/webcam.jpg" width="80"/></td>
<td><strong>Web Camera</strong></td>
<td>Captures real-time frames for MediaPipe landmark processing.</td>
</tr>
</table>
