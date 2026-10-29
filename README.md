# 🛣️ RoadGuard AI: Autonomous Road Damage Surveillance & Neural Voice Alert System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLO-v8s-orange.svg?logo=ultralytics&logoColor=white)](https://docs.ultralytics.com/)
[![Flask](https://img.shields.io/badge/Backend-Flask-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end computer vision and intelligent road infrastructure surveillance platform. Powered by a fine-tuned **YOLOv8s** architecture and served through an interactive **Cyberpunk Amber Operator Dashboard**, the system localizes critical asphalt structural anomalies (potholes, longitudinal/transverse cracks, surface deterioration) in real-time and broadcasts directional **neural audio warnings** to eliminate navigation hazards.

---

## 📌 Key Architectural Highlights

* **Real-Time Asphalt Defect Localization:** Fine-tuned `YOLOv8s` object detection pipeline providing high-precision bounding box extraction and class labeling across challenging road textures and lighting conditions.
* **Dual Voice Alert Mechanism (Zero-Downtime Audio):**
  * **Server-Side Neural Voice:** Generates dynamic, natural acoustic alerts via `Edge-TTS` (`en-US-AriaNeural`).
  * **Client-Side Smart Fallback:** Instant seamless handover to the native browser `Web Speech API` whenever external network bottlenecks occur, ensuring 100% audio availability.
* **Cyberpunk Amber Operator Dashboard:** High-contrast glassmorphism interface featuring interactive confidence thresholding sliders, real-time visual telemetry, and neon-coded spatial defect bounding boxes.
* **Production-Grade Reliability:** Engineered with asynchronous event loops, automated payload compression, and container-ready WSGI configuration.

---

## 📊 Model Evaluation & Benchmarking

Three separate object detection architectures were fine-tuned and benchmarked on identical infrastructure test sets to select the deployment champion:

| Model Architecture | Input Resolution | Parameter Count | mAP@0.5 | mAP@0.5:0.95 | Inference (Batch=1) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLOv8s** | **640×640** | **~11.2M** | **0.4210** | **0.2452** | **18.4 ms** | 🚀 **Production Champion** |
| YOLO11s | 640×640 | ~9.4M | 0.4085 | 0.2310 | 17.9 ms | Evaluated |
| YOLO26s | 640×640 | ~10.1M | 0.3950 | 0.2240 | 18.1 ms | Evaluated |

> **Engineering Verdict:** **YOLOv8s** was designated as the production backbone due to superior localization stability on irregular, low-contrast asphalt fissure boundaries and balanced latency constraints.

---

## 📁 Repository Directory Structure

```text
RoadGuard-AI/
├── assets/
│   └── demo.mp4               # Video demonstration with synchronized audio telemetry
├── app.py                     # Core Flask application & embedded Cyberpunk interface
├── best.pt                    # Fine-tuned YOLOv8s production weights
├── requirements.txt           # Production dependency specifications
├── Procfile                   # Cloud process execution command (Gunicorn)
├── .gitignore                 # Exclusion rules for virtual environments and cache
└── README.md                  # Comprehensive technical documentation
🚀 Local Installation & Quick Start
1. Prerequisites
Python 3.9 or higher

Git installed on your local workstation

2. Clone & Environment Configuration
Bash
# Clone repository
git clone [https://github.com/ZiadWalid44/road-damage-detection-yolov8.git](https://github.com/ZiadWalid44/road-damage-detection-yolov8.git)
cd road-damage-detection-yolov8

# Initialize virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
3. Launch Surveillance Dashboard
Bash
python app.py
Open your browser and navigate to:

Plaintext
[http://127.0.0.1:5000](http://127.0.0.1:5000)
🌐 Cloud Deployment (Render.com)
This repository includes a ready-to-run configuration for permanent 24/7 web hosting on Render:

Link your GitHub account to Render.com.

Create a New Web Service and point it to this repository.

Configure runtime settings:

Environment: Python 3

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app --timeout 120

Instance Type: Free

Trigger the deployment to receive a live, permanent public URL.

🛠️ Technology Stack
Deep Learning Framework: Ultralytics YOLOv8, PyTorch

Computer Vision & Image Processing: OpenCV, Pillow, NumPy

Application Server: Flask, Gunicorn (WSGI)

Speech Synthesis: Edge-TTS, Browser Web Speech API

Front-End Styling: HTML5, CSS3 Glassmorphism (Cyberpunk Amber Palette)

📜 License
This project is open-sourced under the MIT License. See the LICENSE file for details.
