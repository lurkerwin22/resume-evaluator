from flask import Flask, render_template, request
import os
from evaluator import run_resume_evaluation_crew, set_job_post_text, parse_score
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    files = request.files.getlist('resumes')
    job_post = request.form.get('job_post', '')

    if not files or not job_post:
        return "Missing resumes or job description"

    set_job_post_text(job_post)
    evaluations = []

    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            result_text, candidate_name = run_resume_evaluation_crew(filepath)
            score = parse_score(result_text)
            evaluations.append({'name': candidate_name, 'score': score, 'result': result_text})

    # Sort evaluations by score in descending order
    evaluations.sort(key=lambda x: x['score'], reverse=True)

    return render_template('results.html', evaluations=evaluations)

if __name__ == '__main__':
    app.run(debug=True)
