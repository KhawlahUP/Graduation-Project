# Smart Glasses Remote Control (SGRC) 👓✨

![SGRC Prototype](Best%20for%20showing%20results.jpeg)

## 🎓 Graduation Project
This project is a **Senior Graduation Project** from the **Computer Engineering Department** at **Taif University**. It uses AI to control IoT devices via hand gestures.

---

## 📐 System Architecture
This diagram shows how the system works:

```mermaid
graph TD
    User[👤 User] -->|🖐️ Gestures| Camera[📷 Camera]
    Camera -->|🎥 Video Feed| RaspberryPi[🍓 Raspberry Pi]
    RaspberryPi -->|📡 MQTT| ESP8266[📶 ESP8266]
    ESP8266 -->|🔌 Control| IoT_Devices[🏠 IoT Devices]
## ⚙️ Hardware Implementation (3D Designs)
In this section, we present the mechanical parts designed specifically for the SGRC wearable.

![Main Glasses Frame](WhatsApp%20Image%202026-04-13%20at%206.21.30%20PM.jpeg)
**Base Chassis:** This is the primary 3D-printed frame. You can find the source file here: [base_chassis.stl](./hardware/base_chassis.stl).

![Mechanical Components](WhatsApp%20Image%202026-04-13%20at%206.21.30%20PM%20(1).jpeg)
**Movement Mechanism:** Includes the brackets and gears:
* **Motor Brackets:** [motor_bracket_large.stl](./hardware/motor_bracket_large.stl).
* **Pinion Gears:** [pinion_gear_large.stl](./hardware/pinion_gear_large.stl).

---

## ⚡ Simulation & Testing
Before moving to the physical prototype, the system logic and circuit were verified using Proteus.

![Simulation Setup](image_d952aa.png)
**Circuit Validation:** The project includes the full simulation files:
* **Project File:** [sgrc_simulation.pdsprj](./simulation/sgrc_simulation.pdsprj).
* **LCD Libraries:** Supporting DLL files for the display interface.

---

## 📄 Project Documentation
Official reports and presentation materials for the graduation project.

| File Name | Link |
| :--- | :--- |
| **Final Technical Report** | [Download PDF](./docs/Final_Report.pdf) |
| **Project Poster** | [View Poster](./docs/Project_Poster.jpg) |
