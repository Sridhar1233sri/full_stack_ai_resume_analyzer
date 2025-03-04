import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import PyPDF2  # To extract text from PDF

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text.strip()

def analyze_resume_with_gemini(resume_text):
    """Uses Gemini AI to analyze the resume and return a structured response."""
    prompt = f"""
    You are an AI-powered Resume Analyzer. Format your response using Markdown for clear readability.
    
    # 📌 Key Skills Identified:
    - List key skills extracted from the resume.

    ## 📖 Readability Score:
    - Estimated Grade Level: (Provide a grade level readability score)

    ## ⚡ ATS Compatibility Tips:
    ### Formatting:
    - Use a clean font (Arial, Calibri, or Times New Roman).
    - Avoid special characters or symbols in headings and contact info.
    - Maintain consistent date formats (e.g., Month Year - Month Year).
    - Use bullet points for clarity.
    
    ### Keywords:
    - Ensure relevant job keywords are naturally integrated.
    - Use full words and acronyms (e.g., "Database Management" and "DBMS").
    
    ### Structure:
    - Keep it one page (if <10 years of experience).
    - Order sections based on relevance to the target job.
    - Quantify achievements (e.g., "Improved efficiency by 15%").

    ## 📝 Suggested Contact Info Formatting:
    ```
    Sridhar S  
    Address: (Your Corrected Address)  
    Phone: +91 8925107337  
    Email: sridharsri102004@gmail.com  
    LinkedIn: [linkedin.com/in/sridhar-s-044395259](https://linkedin.com/in/sridhar-s-044395259)  
    GitHub: [github.com/Sridhar1233sri](https://github.com/Sridhar1233sri)  
    ```

    ## ✅ Final Recommendations:
    - Improve contact info readability (remove symbols, make links clickable).
    - Begin bullet points with strong action verbs (e.g., Developed, Implemented).
    - Add numbers/metrics to quantify achievements.
    - Tailor the resume for each job description.
    - Consider adding a brief summary/objective at the top.

    **Resume Content for Analysis:**
    ```
    {resume_text}
    ```
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        if response and response.text:
            return response.text.strip()
        else:
            return "⚠️ No meaningful response from Gemini."
    
    except Exception as e:
        return f"⚠️ Error analyzing resume: {str(e)}"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "❌ No file uploaded"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"message": "❌ No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Extract text and analyze with Gemini
    resume_text = extract_text_from_pdf(filepath)
    if not resume_text:
        return jsonify({"message": "❌ Failed to extract text from PDF. Ensure it contains selectable text."}), 400

    analysis = analyze_resume_with_gemini(resume_text)

    return jsonify({"message": "✅ File uploaded successfully!", "analysis": analysis})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
