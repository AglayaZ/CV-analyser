# CV Analyser

Upload your CV as a PDF and get instant AI-powered feedback on how to improve it.

**Live demo:** https://cv-analyser-wnre.onrender.com

## What it does

Analyses your CV and returns:
- An overall score out of 10
- A summary of the CV's current state
- Key strengths
- Areas for improvement
- Missing elements

## Tech used

- Python, Flask — backend
- Google Gemini API — AI analysis
- PyMuPDF — PDF text extraction
- HTML, CSS — frontend
- Deployed on Render

## Run locally

1. Clone the repo and install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file:
   ```
   GEMINI_API_KEY=your-key-here
   ```

3. Run the app:
   ```
   python3 app.py
   ```

4. Open `http://127.0.0.1:5000`
