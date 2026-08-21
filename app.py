from flask import Flask, render_template, request
from google import genai
import fitz
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['cv']
        
        pdf = fitz.open(stream=file.read(), filetype='pdf')
        text = ''
        for page in pdf:
            text += page.get_text()
        
        prompt = f"""You are a professional CV reviewer. Analyse this CV and provide feedback in exactly this format:

Score: [number from 1-10]
Summary: [2-3 sentence overall impression]
Strengths:
- [strength 1]
- [strength 2]
- [strength 3]
Improvements:
- [improvement 1]
- [improvement 2]
- [improvement 3]
Missing:
- [missing element 1]
- [missing element 2]

CV text:
{text}"""
                
        response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
        feedback = response.text
        
        sections = {
            'score': '',
            'summary': '',
            'strengths': [],
            'improvements': [],
            'missing': []
        }

        current_section = None
        for line in feedback.split('\n'):
            line = line.strip()
            if line.startswith('SCORE:'):
                sections['score'] = line.replace('SCORE:', '').strip()
            elif line.startswith('SUMMARY:'):
                sections['summary'] = line.replace('SUMMARY:', '').strip()
            elif line == 'STRENGTHS:':
                current_section = 'strengths'
            elif line == 'IMPROVEMENTS:':
                current_section = 'improvements'
            elif line == 'MISSING:':
                current_section = 'missing'
            elif line.startswith('- ') and current_section:
                sections[current_section].append(line[2:])

        return render_template('results.html', sections=sections)
    
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)