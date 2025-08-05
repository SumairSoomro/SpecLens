
# SpecLens Backend

This is the backend service for **SpecLens**, built with [FastAPI](https://fastapi.tiangolo.com/) and served using [Uvicorn](https://www.uvicorn.org/).

## Contributors
- @varun20020124
---

## 🚀 Getting Started

### 1. Clone the repository
Run in **any terminal location**:
```bash
git clone https://github.com/SumairSoomro/SpecLens.git
cd SpecLens/Backend


⸻

2. Create a virtual environment

Run inside SpecLens/Backend:

python3 -m venv venv


⸻

3. Activate the virtual environment

Run inside SpecLens/Backend:
	•	macOS / Linux

source venv/bin/activate


	•	Windows (PowerShell)

.\venv\Scripts\activate



Once activated, your terminal prompt will show (venv).

⸻

4. Install dependencies

Run inside SpecLens/Backend (while (venv) is active):

pip install -r requirements.txt


⸻

5. Run the development server

Run inside SpecLens/Backend:

uvicorn app.main:app --reload

	•	The server will start at: http://127.0.0.1:8000
	•	Interactive API docs: http://127.0.0.1:8000/docs

⸻

🛠 Health Check

Test the health check endpoint (can be run from any directory while server is running):

curl http://127.0.0.1:8000/health

Expected output:

{"status": "ok"}


⸻

📂 Project Structure

Backend/
│
├── app/
│   ├── main.py         # FastAPI entry point
│   ├── config.py       # Configurations
│   ├── models/         # Database models
│   ├── routes/         # API route definitions
│   ├── services/       # Business logic
│   └── utils/          # Utility functions
│
├── requirements.txt    # Python dependencies
└── venv/               # Virtual environment (excluded from Git)


⸻

💡 Notes
	•	Always activate the virtual environment before running the server.
	•	You must be inside SpecLens/Backend when creating/activating the venv and when running the server.
	•	You can run curl or open the /health endpoint in the browser from any directory once the server is running.
	•	To stop the server, press CTRL+C in the terminal where it’s running.

---

