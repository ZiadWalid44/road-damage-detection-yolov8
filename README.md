1. Repository Setup & Local VerificationEnsure your project directory contains the finalized structure:PlaintextRoadGuard-AI/
├── app.py                  # Primary Flask application (Cyberpunk Amber theme + Web Speech fallback)
├── best.pt                 # Trained YOLOv8s weights file
├── requirements.txt        # Production dependencies
├── Procfile                # Gunicorn deployment command for cloud hosting
├── .gitignore              # Ignores venv, __pycache__, temp files
├── README.md               # Complete project documentation
└── assets/                 # Folder for screen recordings, charts, or GIFs
2. Dependency Configuration (requirements.txt)Plaintextflask
gunicorn
ultralytics
opencv-python-headless
pillow
numpy
edge-tts
3. Git Ignore Configuration (.gitignore)Plaintextvenv/
__pycache__/
*.mp3
.vscode/
.DS_Store
4. Push to GitHubOpen your terminal inside the project directory and run:Bashgit init
git add .
git commit -m "feat: complete road damage AI surveillance system with voice alerts"
git branch -M main
git remote add origin https://github.com/ZiadWalid44/road-damage-detection-yolov8.git
git push -u origin main
5. Deploy Live 24/7 (Render)Go to Render Dashboard and click New + $\to$ Web Service.Connect your RoadGuard-AI repository.Set the following build options:Runtime: Python 3Build Command: pip install -r requirements.txtStart Command: gunicorn app:app --timeout 120Plan: FreeDeploy the service to get your permanent public HTTPS URL.