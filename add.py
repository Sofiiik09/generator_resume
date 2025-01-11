import pdfkit
from flask import Flask, render_template, request, send_file
from datetime import datetime
import os

app = Flask(__name__)

# Local directory to store uploaded resumes
UPLOAD_FOLDER = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

uploaded_file_path = None  # Global variable to store the file path of the uploaded file

pdfkit_config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe") 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data with .get() to avoid KeyError if a key is missing
        name = request.form.get('name', '')  
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        objective = request.form.get('objective', '')
        education_10th_percentage = request.form.get('10th_percentage', '')
        education_12th_percentage = request.form.get('12th_percentage', '')  
        education_cgpa = request.form.get('cgpa', '')
        work_experience = request.form.get('work_experience', '')
        skills = request.form.get('skills', '')

        # Create HTML content for the resume
        resume_content = f"""
        <html>
        <head><title>Resume</title></head>
        <body>
            <h1>{name}</h1>
            <p>Email: {email}</p>
            <p>Phone: {phone}</p>
            <p>Address: {address}</p>
            <h2>Objective</h2>
            <p>{objective}</p>
            <h2>Education</h2>
            <p>CGPA: {education_cgpa}</p>
            <h2>Work Experience</h2>
            <p>{work_experience}</p>
            <h2>Skills</h2>
            <p>{skills}</p>
        </body>
        </html>
        """

        # Generate PDF from the HTML content
        global uploaded_file_path
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{name}_{timestamp}_resume.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Use pdfkit to convert HTML to PDF, with the configuration provided
        pdfkit.from_string(resume_content, file_path, configuration=pdfkit_config)

        uploaded_file_path = file_path

        return render_template('success.html', filename=filename)

    return render_template('resume_upload.html')


@app.route('/download', methods=['GET'])
def download():
    global uploaded_file_path
    if uploaded_file_path:
        return send_file(uploaded_file_path, as_attachment=True)
    return "No file uploaded yet."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
