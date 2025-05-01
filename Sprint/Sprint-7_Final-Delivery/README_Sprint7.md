# 🏧 Sprint 7: Final Testing and System Handover

🗓 **Date:** [2024/04/01]  
🌟 **Goal:** Final system testing, delivery, and documentation handoff.

---

## ✅ Completed Tasks
- Final testing of all functionalities across hardware and software.
- Presented the final product and demonstrated all key features to the client.
- Created a comprehensive user manual and conducted basic training for usage.
---

## 🔌 Hardware Integration Overview

The **ESP8266** microcontroller serves as the WiFi-enabled brain of the system, responsible for sending control signals to connected devices.

- **LEDs**: Each LED has two pins — one for power and one for ground. The control pins are connected to **D3** and **D4**, while all ground lines connect to the **GND** pin on the controller.
- **Relay & Fan**: The **relay** receives ON/OFF commands from the controller to operate the **fan**. A **transistor** is used to step up the controller's 3.3V output to the 5V required by the relay. The transistor has:
  - A control pin connected to **D0**
  - A ground connection via a resistor
  - An output connected to the relay
- **Power Supply**: The **fan** is powered through a relay with:
  - A red cable connected to the relay terminal
  - A black cable connected to the negative terminal of the **battery pack**
- The system is powered by a **battery box**, controlled via a **switch** and protected by a **charging circuit**.



![image](https://github.com/user-attachments/assets/58579a12-4bee-47da-837d-d361b98ed4c6)

![image](https://github.com/user-attachments/assets/2ff3ee9a-86ff-4bad-9adc-a77a1ca48657)


---

## ⚙️ How to Run

```bash
python main.py
```

---

## 📌 Notes
- System handed over successfully.
- Client confirmed satisfaction with the performance, design, and integration.
- No pending issues at the time of delivery.

---

## 📈 Project Status

✅ Finalized and delivered.

---
