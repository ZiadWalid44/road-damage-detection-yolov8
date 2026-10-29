import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO

# Page Configuration
st.set_page_config(
    page_title="RoadGuard AI | Surveillance System",
    page_icon="🛣️",
    layout="wide"
)

# Custom Cyberpunk Amber Styles
st.markdown("""
<style>
    .metric-box {
        background-color: #161b22;
        border: 1px solid #ffaa00;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 0 10px rgba(255, 170, 0, 0.2);
    }
    .neon-text {
        color: #ffaa00;
        font-weight: 700;
        text-shadow: 0 0 8px rgba(255, 170, 0, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='neon-text'>🛣️ RoadGuard AI: Asphalt Defect Surveillance</h1>", unsafe_allow_html=True)
st.caption("Real-time automated asphalt structural damage localization powered by fine-tuned YOLOv8s.")

@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# Sidebar Telemetry
st.sidebar.markdown("<h2 class='neon-text'>⚙️ System Configuration</h2>", unsafe_allow_html=True)
conf_threshold = st.sidebar.slider("Confidence Threshold", min_value=0.10, max_value=1.00, value=0.25, step=0.05)
enable_audio = st.sidebar.checkbox("Enable Neural Audio Alerts", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**Engine:** YOLOv8s Architecture  \n**Weights:** `best.pt`  \n**Status:** `Active Surveillance`")

uploaded_file = st.file_uploader("Upload Surface Inspection Frame", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns(2)

if uploaded_file is not None:
    input_image = Image.open(uploaded_file).convert("RGB")
    
    with col1:
        st.markdown("<h4 class='neon-text'>Source Feed</h4>", unsafe_allow_html=True)
        st.image(input_image, use_container_width=True)

    with col2:
        st.markdown("<h4 class='neon-text'>YOLOv8 Telemetry Overlay</h4>", unsafe_allow_html=True)
        with st.spinner("Analyzing surface morphology..."):
            img_np = np.array(input_image)
            results = model.predict(source=img_np, conf=conf_threshold)
            res_plotted = results[0].plot()
            st.image(res_plotted, use_container_width=True)

        boxes = results[0].boxes
        num_detections = len(boxes)

        st.markdown(f"""
        <div class="metric-box">
            <h4>Detection Summary</h4>
            <p>Total Anomalies Identified: <b style="color: #ffaa00;">{num_detections}</b></p>
            <p>Target Pipeline: <b style="color: #ffaa00;">YOLOv8s Inspector</b></p>
        </div>
        """, unsafe_allow_html=True)

        if num_detections > 0 and enable_audio:
            speech_text = f"Warning. Road damage detected. {num_detections} structural defects identified."
            audio_html = f"""
            <script>
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const msg = new SpeechSynthesisUtterance('{speech_text}');
                    msg.rate = 1.0;
                    msg.pitch = 1.0;
                    window.speechSynthesis.speak(msg);
                }}
            </script>
            """
            st.components.v1.html(audio_html, height=0)