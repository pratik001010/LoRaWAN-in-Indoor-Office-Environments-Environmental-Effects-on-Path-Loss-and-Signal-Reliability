# LoRaWAN in Indoor Office Environments  
### *Environmental Effects on Path Loss & Signal Reliability*  
*A Machine Learning and Real-Time Dashboard Approach*

---

## 📘 Overview  
This project investigates how **indoor environmental conditions**—walls, humidity, CO₂, PM₂.₅, pressure, and temperature—affect **LoRaWAN signal reliability and path loss**.  
It combines **data collection**, **machine learning**, and **real-time visualization** into a unified IoT analysis pipeline.

> Conducted under the *Erasmus Mundus Joint Master’s Program – Embedded Intelligence and Nano Systems Engineering (EMINENT)* at the **University of Siegen**.

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page1.png)

---

## 🎯 Objectives  
- Evaluate **LoRaWAN performance** under various indoor conditions.  
- Build supervised ML models (MLR, RF, XGBoost) for **path-loss prediction**.  
- Create a **real-time Flutter + MQTT dashboard** for signal monitoring.  
- Export lightweight **TFLite models** for on-node inference.  

---

## 🧩 Experimental Setup  
- **Location:** Multi-room office (LOS + NLOS)  
- **Band:** EU868  **Period:** 4 months (≈ 1.3 M samples)  
- **Interval:** 1 sample/min  **Device height:** 0.8 m  **Gateway:** central (1 m)  

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page7.png)  
*Experiment layout and device distribution.*

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page%208%20.png)  
*Gateway and sensor nodes in the office.*

---

### 🔧 Devices Used

#### End Devices (ED0–ED5)
| Component | Description |
|------------|-------------|
| **Arduino MKR WAN 1310** | LoRaWAN Class-A (EU868) end node |
| **Adafruit BME280** | Pressure, Temperature, Humidity |
| **Sensirion SCD41** | CO₂ Sensor |
| **Sensirion SPS30** | PM₂.₅ Sensor |
| **Antenna** | 3 dBi rubber duck |
| **3D Case** | Ventilated enclosure for airflow |

#### Gateway
| Spec | Details |
|-------|----------|
| **Model** | Kerlink Wirnet iFemtoCell |
| **Gain** | 3 – 5 dBi |
| **Connectivity** | Ethernet → TTN |
| **Function** | Uplink forwarding via MQTT |

---

### 📍 Deployment Layout
| Device | Distance (m) | Brick Walls | Wooden Partitions |
|---------|--------------|-------------|-------------------|
| ED0 | 10 | 0 | 0 |
| ED1 | 8 | 1 | 0 |
| ED2 | 25 | 0 | 2 |
| ED3 | 18 | 1 | 2 |
| ED4 | 37 | 0 | 5 |
| ED5 | 40 | 2 | 2 |

---

## 🤖 Machine Learning Framework  

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page11.png)  
*Decision-Tree, Random Forest & XGBoost overview.*

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page12.png)  
*Bias-Variance trade-off and Cross-Validation concepts.*

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page13.png)  
*Supervised ML pipeline.*

| Model | R² | RMSE (dB) | Remarks |
|-------|----:|----------:|----------|
| MLR | 0.81 | 8.26 | Linear baseline |
| Random Forest | 0.94 | 4.68 | Good generalization |
| **XGBoost** | **0.95** | **3.84** | Best accuracy |

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page14.png)  
*Predicted vs Actual path-loss plots.*

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page15%20.png)  
*Comparative performance table.*

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page16.png)  
*Study limitations.*

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page17.png)  
*Conclusion – XGBoost outperforms others.*

---

## 💻 Dashboard and IoT Integration  

### Why a Dashboard ?  
![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page18.png)  
*Left – signal equations; Right – real-time Flutter dashboard.*

**Problem:** Hard-to-interpret raw data.  
**Solution:** Interactive Flutter UI + live MQTT stream.

---

## 🌐 IoT Architecture  
![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page19.png)

**Layers**
1️⃣ Perception – Sensor data capture  
2️⃣ Network – LoRaWAN / MQTT connectivity  
3️⃣ Processing – Cloud inference  
4️⃣ Application – Visualization via dashboard  

![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page20.png)  
*Processing Layer – TTN + MQTT broker integration.*

---

## ⚙️ Implementation Steps  
![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page22.png)

1️⃣ **Wireframing (Figma)** – screen flow design  
2️⃣ **Language Selection** – Flutter for cross-platform dev  
3️⃣ **MQTT Config** – live data from TTN  
4️⃣ **Login & Auth** – secure access control  
5️⃣ **Frontend Build** – responsive Flutter UI  

---

## 🧠 Results Demo  

**Dashboard Login**  
![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/appdesign.gif)

**Live Simulation – Path Loss Calculation**  
![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/customize.gif)

---

## 🚀 Future Scope – What Comes Next  
![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page26.png)
![](https://github.com/pratik001010/LoRaWAN-in-Indoor-Office-Environments-Environmental-Effects-on-Path-Loss-and-Signal-Reliability/blob/c49f70b647063cd5e6f3f6ec71f7535e0c2b9895/lora/page27.png)

### 1️⃣ Mobile & Web App Deployment  
- Extend Flutter dashboard to Android/iOS and Web.  
- Enable real-world deployment and scaling.  

### 2️⃣ Real-Time ML Inference  
- Integrate `.pkl` models (e.g. XGBoost) for live signal prediction.  
- Cloud/Edge computing for scalable ML deployment.  

---

## 🛠️ Getting Started  
### Prerequisites  
- TTN App + Registered Devices  
- MQTT Credentials  
- Flutter ≥ 3.x  
- Python ≥ 3.10 (`xgboost`, `sklearn`, `tensorflow`)

### Setup  
```
git clone https://github.com/pratik001010/LoRaWAN-Indoor-Pathloss-Analyzer
cd LoRaWAN-Indoor-Pathloss-Analyzer
```

```
# MQTT .env configuration
MQTT_HOST=eu1.cloud.thethings.network
MQTT_PORT=8883
MQTT_USERNAME=<ttn-app-id>
MQTT_PASSWORD=<ttn-api-key>
MQTT_TOPIC=v3/<ttn-app-id>/devices/+/up
```

```
# Run Dashboard
flutter pub get  
flutter run -d windows  # or macos/linux
```

```
# Train and Export Model
cd ml  
python train_xgboost.py  
python distill_to_tflite.py
```

---

## ✅ Key Outcomes  
- Indoor environment strongly impacts RSSI / SNR variation.  
- XGBoost model achieved **R² = 0.95** with RMSE ≈ 3.8 dB.  
- Flutter dashboard enabled **real-time visualization** and user interaction.  
- Workflow bridged **LoRaWAN + ML + IoT Visualization** in one ecosystem.  

---

## 👥 Team  
**Project Title:** LoRaWAN Indoor Signal Reliability and Path-Loss Modeling  
**University:** University of Siegen – Erasmus Mundus EMINENT  

| Name | Role |
|-------|-------|
| 🧑‍💻 Pratik Khadka | Dashboard & ML Integration |
| 👨‍💻 Vincent Mwenda Mworia | Field Deployment & Data Analysis |
| 👨‍🏫 Supervisor: Nahshon M. Obiri | Project Mentor |

---

📄 **Reference**  
Obiri, N. M., & Van Laerhoven, K. (2024). *A Comprehensive Data Description for LoRaWAN Path Loss Measurements in an Indoor Office Setting.* IEEE Access. DOI: 10.1109/ACCESS.2024.0429000
