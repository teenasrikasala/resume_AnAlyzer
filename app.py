import os
import json
from PyPDF2 import PdfReader
from google import genai
from google.genai import types
from flask import Flask,request,jsonify,render_template
app=Flask(__name__)
client=genai.Client(api_key=os.getenv("Gemini_api_key3"))
@app.route('/')
def home():
    return render_template('UI.html')
@app.route('/analyze',methods=['POST'])
def analyze():
    try:
        jd=request.form['job_description']
        c_re=request.files['resume']
        print(c_re.filename)
        pdf_reader=PdfReader(c_re)
        resume_text=''
        for page in pdf_reader.pages:
            text=page.extract_text()
            if text:
                resume_text+=text+'\n'
        prompt=f"""
        You are an ATS Resume Analyzer.
        Analyze the resume against the job description.

        Job description:
        {jd} and
        resume:
        {resume_text}
        you should give output only in json format like this
        {{
            "atsscore":85,
            "skills_matching":
            [
                "Python",
                "SQL"
            ],
            "missingskills":
            [
                "AWS",
                "Docker"
            ],
            "suggestions":
            [
                "learn AWS",
                "learn Docker"
            ],
            "summary":"short summary"
        }}
        """
        response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=1000)
        )
        result_text=response.text.strip()
        result_text=result_text.replace("```json","")
        result_text=result_text.replace("```","").strip()
        try:
            result=json.loads(result_text)
        except json.JSONDecodeError:
            result={
                 "atsscore":0,
                 "skills_matching":[],
                 "missingskills":[],
                 "suggestions":[],
                 "summary":"API error occured to analyze"
            }
        return jsonify(result)
    except Exception as e:
        print("Error:",e)
        return jsonify({
                 "atsscore":0,
                 "skills_matching":[],
                 "missingskills":[],
                 "suggestions":[],
                 "summary":"API error occured to analyze resume"
        }),500
if __name__=="__main__":
    app.run(debug=True)        
                