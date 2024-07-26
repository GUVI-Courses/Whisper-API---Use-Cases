from flask import Flask, request, jsonify, send_from_directory
import openai
import os

from fpdf import FPDF


# Initialize Flask app
app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory('templates','index.html')

@app.route('/generate-resume',methods=['POST'])
def generate_resume():
    data= request.get_json()
    name=data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    profile = data.get('profile')
    role = data.get('role')
    skills = data.get('skills')
    workExperience1 = data.get('workExperience1')
    workExperience2 = data.get('workExperience2')
    education = data.get('education')
    internship = data.get('internship')
    hobbies = data.get('hobbies')
    certifications = data.get('certifications')
    topProjects = data.get('topProjects')
    print(name,email,phone)

    try:
        prompt= (
            f"Create a professional resume with the following details:\n\n"
            f"Name: {name}\n"
                  f"Email: {email}\n"
                  f"Phone: {phone}\n"
                  f"Address: {address}\n\n"
                  f"Profile Description:\n{profile}\n\n"
                  f"Role:\n{role}\n\n"
                  f"Skills:\n{skills}\n\n"
                  f"Work Experience 1:\n{workExperience1}\n\n"
                  f"Work Experience 2:\n{workExperience2}\n\n"
                  f"Education:\n{education}\n\n"
                  f"Internship:\n{internship}\n\n"
                  f"Hobbies:\n{hobbies}\n\n"
                  f"Certifications:\n{certifications}\n\n"
                  f"Top Projects:\n{topProjects}\n\n"
                   f"Format the resume with clear headings, bullet points for work experience, and concise language.")
        
        print(prompt)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a resume formatting expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        print(response)

        format_resume=response.choices[0].message['content'].strip()
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font("Arial",size=10)

        pdf.multi_cell(0,10,format_resume)

        pdf_output_path='resume.pdf'
        pdf.output(pdf_output_path)
        return jsonify({
            'resume': {
                'name': name,
                'email': email,
                'phone': phone,
                'address': address,
                'profile': profile,
                'role': role,
                'skills': skills,
                'workExperience1': workExperience1,
                'workExperience2': workExperience2,
                'education': education,
                'internship': internship,
                'hobbies': hobbies,
                'certifications': certifications,
                'topProjects': topProjects
            }
        })
    except Exception as e:
        return jsonify({'error':str(e)}),500

@app.route('/download-pdf', methods=['GET'])
def download_pdf():
    return send_from_directory('.', 'resume.pdf')




if __name__ == '__main__':
    app.run(debug=True)
