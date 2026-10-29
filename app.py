import os
import cv2
import asyncio
import base64
import traceback
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template_string
import edge_tts
from ultralytics import YOLO

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file 'best.pt' not found at {MODEL_PATH}.")

model = YOLO(MODEL_PATH)

# باليت ألوان النيون البركانية (BGR)
NEON_PALETTE = [
    (0, 140, 255),    # Deep Neon Orange
    (0, 215, 255),    # Bright Amber / Gold
    (0, 69, 255),     # Crimson Red-Orange
    (0, 255, 200),    # Bright Mint
    (50, 50, 255),    # High-intensity Red
    (0, 230, 255),    # Electric Yellow
    (180, 0, 255)     # Ultraviolet Flame
]

def try_generate_edge_voice(text: str, path: str) -> bool:
    """محاولة توليد الصوت عبر edge-tts مع معالجة آمنة لفشل الاتصال"""
    async def _runner():
        comm = edge_tts.Communicate(text, voice="en-US-AriaNeural", rate="+10%")
        await comm.save(path)

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait_for(_runner(), timeout=4.0))
        loop.close()
        return True
    except Exception as e:
        print(f"[Warning] Edge-TTS offline or timed out: {e}. Switching to Client-Side Speech.")
        return False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Road Damage AI Surveillance</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { 
            background: radial-gradient(circle at top, #1c100b 0%, #09090b 100%); 
            color: #f4f4f5; 
            padding: 30px 20px; 
            min-height: 100vh;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { 
            font-size: 2.3rem; 
            background: linear-gradient(90deg, #f97316, #ef4444);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 8px; 
        }
        .header p { color: #a1a1aa; font-size: 1rem; }
        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
        
        .card { 
            background: rgba(24, 24, 27, 0.85); 
            backdrop-filter: blur(12px);
            border: 1px solid rgba(249, 115, 22, 0.2); 
            border-radius: 14px; 
            padding: 24px; 
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px -3px rgba(249, 115, 22, 0.05); 
        }
        .card h2 { 
            font-size: 1.15rem; 
            color: #fed7aa; 
            margin-bottom: 16px; 
            border-bottom: 1px solid rgba(249, 115, 22, 0.2); 
            padding-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .input-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; font-size: 0.85rem; color: #fdba74; text-transform: uppercase; letter-spacing: 0.5px; }
        
        input[type="file"] { 
            width: 100%; 
            padding: 12px; 
            background: #111113; 
            border: 1px dashed rgba(249, 115, 22, 0.4); 
            border-radius: 8px; 
            color: #d4d4d8; 
            cursor: pointer; 
            transition: all 0.2s ease;
        }
        input[type="file"]:hover { 
            border-color: #f97316; 
            background: #17171a; 
        }
        
        .slider-container { display: flex; align-items: center; gap: 12px; }
        input[type="range"] { 
            flex-grow: 1; 
            accent-color: #f97316; 
            cursor: pointer;
        }
        
        .btn { 
            width: 100%; 
            padding: 14px; 
            background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%); 
            border: none; 
            border-radius: 8px; 
            color: white; 
            font-size: 1rem; 
            font-weight: 700; 
            cursor: pointer; 
            box-shadow: 0 4px 15px rgba(234, 88, 12, 0.35);
            transition: all 0.2s ease; 
        }
        .btn:hover { 
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(234, 88, 12, 0.5);
            filter: brightness(1.1);
        }
        .btn:disabled { 
            background: #27272a; 
            color: #71717a;
            box-shadow: none;
            cursor: not-allowed; 
            transform: none;
        }
        
        .result-box { 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            min-height: 270px; 
            background: #111113; 
            border-radius: 8px; 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            overflow: hidden; 
            margin-bottom: 16px; 
        }
        .result-box img { max-width: 100%; height: auto; display: block; border-radius: 6px; }
        
        .status-badge { 
            width: 100%; 
            padding: 12px; 
            border-radius: 6px; 
            background: #111113; 
            border-left: 4px solid #f97316; 
            font-size: 0.95rem; 
            margin-bottom: 16px; 
        }
        
        audio { 
            width: 100%; 
            height: 40px; 
            outline: none; 
            filter: invert(0.9) hue-rotate(160deg);
        }
        @media(max-width: 768px) { .dashboard { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 Road Damage AI Surveillance System</h1>
            <p>Real-time asphalt condition assessment with automated neural voice alerts.</p>
        </div>
        <div class="dashboard">
            <div class="card">
                <h2>⚙️ Control Panel</h2>
                <div class="input-group">
                    <label>Select Road Image</label>
                    <input type="file" id="imageInput" accept="image/*">
                </div>
                <div class="input-group">
                    <label>Confidence Threshold: <span id="confVal" style="color: #f97316; font-weight: bold;">0.35</span></label>
                    <div class="slider-container">
                        <input type="range" id="confSlider" min="0.1" max="1.0" step="0.05" value="0.35" oninput="document.getElementById('confVal').innerText = this.value">
                    </div>
                </div>
                <button class="btn" id="analyzeBtn" onclick="analyzeRoad()">Analyze Road 🚀</button>
            </div>
            <div class="card">
                <h2>🎯 Inspection Results</h2>
                <div class="result-box" id="resultContainer">
                    <span style="color: #52525b;">Awaiting road image...</span>
                </div>
                <div class="status-badge" id="statusBadge">Status: Ready</div>
                <audio id="audioPlayer" controls style="display:none;"></audio>
            </div>
        </div>
    </div>

    <script>
        function playBrowserSpeech(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                utterance.rate = 1.05;
                window.speechSynthesis.speak(utterance);
            }
        }

        async function analyzeRoad() {
            const fileInput = document.getElementById('imageInput');
            const conf = document.getElementById('confSlider').value;
            const btn = document.getElementById('analyzeBtn');
            const status = document.getElementById('statusBadge');
            const container = document.getElementById('resultContainer');
            const audio = document.getElementById('audioPlayer');

            if (!fileInput.files[0]) {
                alert('Please upload an image first.');
                return;
            }

            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            formData.append('conf', conf);

            btn.disabled = true;
            btn.innerText = 'Analyzing...';
            status.innerText = 'Running inference & neural voice generation...';

            try {
                const res = await fetch('/predict', { method: 'POST', body: formData });
                const data = await res.json();

                if (!res.ok || data.error) {
                    alert(data.error || 'Server error occurred during inference.');
                } else {
                    container.innerHTML = `<img src="data:image/jpeg;base64,${data.image}" alt="Detection">`;
                    status.innerHTML = data.summary;

                    // تشغيل الصوت: إن وجد ملف سيرفر يتم تشغيله، وإلا ينطق المتصفح فوراً
                    if (data.audio) {
                        audio.src = `data:audio/mp3;base64,${data.audio}`;
                        audio.style.display = 'block';
                        audio.play().catch(() => playBrowserSpeech(data.speech_text));
                    } else {
                        playBrowserSpeech(data.speech_text);
                    }
                }
            } catch (err) {
                alert('Error running inference. Check server console.');
                console.error(err);
            } finally {
                btn.disabled = false;
                btn.innerText = 'Analyze Road 🚀';
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]
        conf_score = float(request.form.get("conf", 0.35))

        pil_img = Image.open(file.stream).convert("RGB")
        
        max_dim = 1024
        w, h = pil_img.size
        if max(w, h) > max_dim:
            scale = max_dim / max(w, h)
            pil_img = pil_img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)

        img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        detections = model.predict(source=img_bgr, conf=conf_score, verbose=False)[0]

        found_labels = []
        if detections.boxes is not None and len(detections.boxes) > 0:
            for box in detections.boxes:
                cid = int(box.cls[0])
                conf = float(box.conf[0])
                cname = model.names[cid]
                found_labels.append(cname)

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                color = NEON_PALETTE[cid % len(NEON_PALETTE)]

                cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color, 3)
                tag = f"{cname} {conf:.1%}"
                (tw, th), _ = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(img_bgr, (x1, max(y1 - 25, 0)), (x1 + tw + 6, max(y1, 25)), color, -1)
                cv2.putText(img_bgr, tag, (x1 + 3, max(y1 - 7, 18)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)

            count = len(detections.boxes)
            unique_damages = ", ".join(sorted(set(found_labels)))
            speech_text = f"Caution! Detected {count} road damages: {unique_damages}."
            summary = f"🚨 <b style='color:#f97316;'>{count} damage(s) detected:</b> {unique_damages}"
        else:
            speech_text = "The road surface is clear. Safe journey."
            summary = "✅ <b style='color:#22c55e;'>Road surface looks safe and clear.</b>"

        _, buffer = cv2.imencode(".jpg", img_bgr)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        # توليد الصوت مع نظام الأمان
        audio_file = os.path.join(BASE_DIR, "temp_alert.mp3")
        voice_ok = try_generate_edge_voice(speech_text, audio_file)

        audio_base64 = None
        if voice_ok and os.path.exists(audio_file):
            with open(audio_file, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode("utf-8")

        return jsonify({
            "image": img_base64,
            "summary": summary,
            "speech_text": speech_text,
            "audio": audio_base64
        })

    except Exception as e:
        print("--- Exception in /predict ---")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)