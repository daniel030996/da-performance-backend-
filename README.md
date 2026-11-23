# DA PERFORMANCE Backend

Simple FastAPI server that the mobile app calls for diagnosis.

## Quick free hosting (recommended: Render)

1. Go to https://render.com and sign up (free).
2. Click **New +** → **Web Service**.
3. Connect a GitHub repo (or use “Public Git repository” / upload).
4. Or easiest: create a new GitHub repo, upload these two files (`main.py` and `requirements.txt`), then connect it on Render.
5. On Render set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy. Copy the URL Render gives you (e.g. `https://da-performance-xxxx.onrender.com`).
7. In the phone app HTML, find the line:
   `const LIVE_SEARCH_ENDPOINT = "..."`
   and change it to:
   `const LIVE_SEARCH_ENDPOINT = "https://your-render-url.onrender.com/diagnose";`

Once that is done the app will use the live backend automatically.

## Local test (if you ever have a computer)
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Then open http://localhost:8000/docs
