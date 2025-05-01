## 🧠 5.8 Run Module

The **Run Module** acts as the central controller, integrating:
- Hand-tracking module
- Detector module
- IoT device control (via ESP)

It continuously:
1. Captures video frames.
2. Interprets gestures.
3. Detects objects.
4. Sends MQTT commands to an ESP controlling LEDs and a fan.

This real-time interaction enables gesture-based control of devices like lights and fans via lightweight **MQTT protocol**.

### 🔄 MQTT Commands Example

| Command Sent from RPi | MQTT Topic         | Payload    | ESP Action                     |
|-----------------------|--------------------|------------|--------------------------------|
| All LEDs ON           | `/leds/esp8266`    | `ALLON`    | All LEDs turned ON             |
| All LEDs OFF          | `/leds/esp8266`    | `ALLOFF`   | All LEDs turned OFF            |

The ESP8266 receives the message and sets GPIO pins `HIGH` or `LOW` to control connected devices.

---

## ⚙️ ESP Code Overview

The ESP8266 firmware uses:
- `ESP8266WiFi.h` – for WiFi connection
- `Adafruit_MQTT.h` – for MQTT communication

It handles message subscriptions and executes the received commands by toggling digital pins connected to:
- LEDs
- Fan (via transistor + relay)

---

## 📈 5.9 Results

### ✋ 5.9.1 Hand Gesture Control

Using gestures (like raising fingers), users can wirelessly:
- Turn LEDs ON/OFF
- Control the fan

#### 🔘 Gesture Examples:

<div align="center">

  <h4>Led 1 On</h4>
  <img src="Diagram/Led%201%20On.jpg" width="200"/>

  <h4>Led 1 Off</h4>
  <img src="Diagram/Led%201%20Off.jpg" width="200"/>

  <h4>All LEDs On</h4>
  <img src="Diagram/All%20Leds%20On.jpg" width="200"/>

  <h4>All LEDs Off</h4>
  <img src="Diagram/All%20Leds%20Off.jpg" width="200"/>

  <h4>Fan On</h4>
  <img src="Diagram/Fan%20On.jpg" width="200"/>

  <h4>Fan Off</h4>
  <img src="Diagram/Fan%20Off.jpg" width="200"/>

  <h4>Led 2 On</h4>
  <img src="Diagram/Led%202%20On.jpg" width="200"/>

  <h4>Led 2 Off</h4>
  <img src="Diagram/Led%202%20Off.jpg" width="200"/>

</div>


---

### 🔍 5.9.2 Object Recognition

Smart glasses detect nearby objects and provide **real-time feedback**, enabling smart interaction.

<div align="center">
  <h4>Figure 5.8 – Object Recognition Samples</h4>
  <img src="Diagram/Object Recognition Samples.jpg" width="400"/>
</div>
