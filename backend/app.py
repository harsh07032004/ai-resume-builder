from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
import tempfile
import json
from jinja2 import Template
from datetime import datetime
import uuid
from transformers import pipeline
import logging
from job_optimizer import JobDescriptionOptimizer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize job optimizer
try:
    job_optimizer = JobDescriptionOptimizer()
    OPTIMIZER_ENABLED = True
    logger.info("Job optimizer initialized successfully")
except Exception as e:
    logger.warning(f"Job optimizer initialization failed: {e}")
    job_optimizer = None
    OPTIMIZER_ENABLED = False

# Initialize AI text enhancement pipeline (optional)
try:
    enhancer = pipeline("text2text-generation", model="t5-small")
    AI_ENABLED = True
    logger.info("AI text enhancement enabled")
except Exception as e:
    logger.warning(f"AI enhancement disabled: {e}")
    AI_ENABLED = False

def enhance_text(text, max_length=100):
    """Enhance text using AI if available"""
    if not AI_ENABLED or not text.strip():
        return text
    
    try:
        # Simple prompt for text enhancement
        prompt = f"Improve this professional description: {text}"
        result = enhancer(prompt, max_length=max_length, num_return_sequences=1)
        return result[0]['generated_text'] if result else text
    except Exception as e:
        logger.warning(f"Text enhancement failed: {e}")
        return text

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "ai_enabled": AI_ENABLED,
        "optimizer_enabled": OPTIMIZER_ENABLED
    })

@app.route('/generate', methods=['POST'])
def generate_resume():
    """Generate resume PDF from form data"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Enhance descriptions with AI if enabled
        if data.get('enhance_with_ai', False) and AI_ENABLED:
            # Enhance work experience descriptions
            if 'work_experience' in data:
                for exp in data['work_experience']:
                    if exp.get('description'):
                        exp['description'] = enhance_text(exp['description'])
            
            # Enhance project descriptions
            if 'projects' in data:
                for project in data['projects']:
                    if project.get('description'):
                        project['description'] = enhance_text(project['description'])
        
        # Generate PDF
        pdf_path = create_resume_pdf(data)
        
        if pdf_path and os.path.exists(pdf_path):
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"{data['name'].replace(' ', '_')}_resume.pdf",
                mimetype='application/pdf'
            )
        else:
            return jsonify({"error": "Failed to generate PDF"}), 500
            
    except Exception as e:
        logger.error(f"Error generating resume: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview_resume():
    """Generate HTML preview of the resume"""
    try:
        data = request.get_json()
        html_content = create_resume_html(data)
        return jsonify({"html": html_content})
    except Exception as e:
        logger.error(f"Error generating preview: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze-job', methods=['POST'])
def analyze_job_description():
    """Analyze job description and extract key information"""
    try:
        if not OPTIMIZER_ENABLED:
            return jsonify({"error": "Job optimizer not available"}), 503
        
        data = request.get_json()
        job_description = data.get('job_description', '')
        
        if not job_description.strip():
            return jsonify({"error": "Job description is required"}), 400
        
        # Analyze job description
        analysis = job_optimizer.analyze_job_description(job_description)
        
        return jsonify({
            "analysis": analysis,
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Error analyzing job description: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/optimize-resume', methods=['POST'])
def optimize_resume():
    """Optimize resume based on job description"""
    try:
        if not OPTIMIZER_ENABLED:
            return jsonify({"error": "Job optimizer not available"}), 503
        
        data = request.get_json()
        resume_data = data.get('resume_data', {})
        job_description = data.get('job_description', '')
        
        # Validate required fields
        if not job_description.strip():
            return jsonify({"error": "Job description is required"}), 400
        
        if not resume_data.get('name') or not resume_data.get('email'):
            return jsonify({"error": "Resume data with name and email is required"}), 400
        
        # Analyze job description first
        job_analysis = job_optimizer.analyze_job_description(job_description)
        
        # Generate optimization suggestions
        optimization_result = job_optimizer.optimize_resume(resume_data, job_analysis)
        
        return jsonify({
            "optimization": optimization_result,
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Error optimizing resume: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/apply-suggestions', methods=['POST'])
def apply_suggestions():
    """Apply optimization suggestions to resume data"""
    try:
        data = request.get_json()
        resume_data = data.get('resume_data', {})
        suggestions = data.get('suggestions', {})
        selected_improvements = data.get('selected_improvements', [])
        
        # Apply selected experience improvements
        for improvement in selected_improvements:
            if improvement.get('type') == 'experience' and 'index' in improvement:
                idx = improvement['index']
                if idx < len(resume_data.get('work_experience', [])):
                    resume_data['work_experience'][idx]['description'] = improvement['improved']
        
        # Apply selected project improvements
        for improvement in selected_improvements:
            if improvement.get('type') == 'project' and 'index' in improvement:
                idx = improvement['index']
                if idx < len(resume_data.get('projects', [])):
                    resume_data['projects'][idx]['description'] = improvement['improved']
        
        # Add suggested skills if requested
        if data.get('add_suggested_skills', False):
            current_skills = set(resume_data.get('skills', []))
            suggested_skills = suggestions.get('skills_to_add', [])
            new_skills = current_skills.union(set(suggested_skills))
            resume_data['skills'] = list(new_skills)
        
        return jsonify({
            "optimized_resume": resume_data,
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Error applying suggestions: {e}")
        return jsonify({"error": str(e)}), 500

def create_resume_pdf(data):
    """Create PDF resume from data using LaTeX"""
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = os.path.join(temp_dir, "resume.tex")
            pdf_file = os.path.join(temp_dir, "resume.pdf")
            
            # Generate LaTeX content
            latex_content = generate_latex(data)
            
            # Write LaTeX file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Compile LaTeX to PDF
            result = subprocess.run([
                'pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"LaTeX compilation failed: {result.stderr}")
                return None
            
            # Copy PDF to a permanent location
            output_dir = os.path.join(os.path.dirname(__file__), 'generated')
            os.makedirs(output_dir, exist_ok=True)
            
            output_pdf = os.path.join(output_dir, f"resume_{uuid.uuid4().hex[:8]}.pdf")
            subprocess.run(['cp', pdf_file, output_pdf])
            
            return output_pdf
            
    except Exception as e:
        logger.error(f"Error creating PDF: {e}")
        return None

def create_resume_html(data):
    """Create HTML preview of the resume"""
    html_template = """
    <div class="max-w-4xl mx-auto bg-white p-8 shadow-lg">
        <div class="text-center mb-6">
            <h1 class="text-3xl font-bold text-gray-800">{{ name }}</h1>
            <p class="text-gray-600">{{ email }}</p>
            {% if phone %}
            <p class="text-gray-600">{{ phone }}</p>
            {% endif %}
        </div>
        
        {% if education %}
        <div class="mb-6">
            <h2 class="text-xl font-semibold text-gray-800 border-b-2 border-gray-300 pb-2 mb-4">Education</h2>
            {% for edu in education %}
            <div class="mb-3">
                <div class="flex justify-between">
                    <h3 class="font-semibold">{{ edu.degree }}</h3>
                    <span class="text-gray-600">{{ edu.year }}</span>
                </div>
                <p class="text-gray-700">{{ edu.institution }}</p>
                {% if edu.gpa %}
                <p class="text-gray-600">GPA: {{ edu.gpa }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if work_experience %}
        <div class="mb-6">
            <h2 class="text-xl font-semibold text-gray-800 border-b-2 border-gray-300 pb-2 mb-4">Work Experience</h2>
            {% for exp in work_experience %}
            <div class="mb-4">
                <div class="flex justify-between">
                    <h3 class="font-semibold">{{ exp.position }}</h3>
                    <span class="text-gray-600">{{ exp.duration }}</span>
                </div>
                <p class="text-gray-700 font-medium">{{ exp.company }}</p>
                {% if exp.description %}
                <p class="text-gray-600 mt-2">{{ exp.description }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if projects %}
        <div class="mb-6">
            <h2 class="text-xl font-semibold text-gray-800 border-b-2 border-gray-300 pb-2 mb-4">Projects</h2>
            {% for project in projects %}
            <div class="mb-4">
                <h3 class="font-semibold">{{ project.title }}</h3>
                {% if project.description %}
                <p class="text-gray-600 mt-2">{{ project.description }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if skills %}
        <div class="mb-6">
            <h2 class="text-xl font-semibold text-gray-800 border-b-2 border-gray-300 pb-2 mb-4">Skills</h2>
            <div class="flex flex-wrap gap-2">
                {% for skill in skills %}
                <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">{{ skill }}</span>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
    """
    
    template = Template(html_template)
    return template.render(**data)

def generate_latex(data):
    """Generate LaTeX content from form data"""
    latex_template = r"""
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{fontawesome5}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\pdfgentounicode=1

\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

\begin{center}
    \textbf{\Huge \scshape {{ name }}} \\ \vspace{1pt}
    {% if phone %}\small {{ phone }} $|$ {% endif %}
    \href{mailto:{{ email }}}{\underline{{ "{" }}{{ email }}{{ "}" }}} {% if linkedin %}$|$ 
    \href{{ "{" }}{{ linkedin }}{{ "}" }}{\underline{{ "{" }}LinkedIn{{ "}" }}}{% endif %}
\end{center}

{% if education %}
\section{Education}
  \resumeSubHeadingListStart
    {% for edu in education %}
    \resumeSubheading
      {{ "{" }}{{ edu.degree }}{{ "}" }}{{ "{" }}{{ edu.year }}{{ "}" }}
      {{ "{" }}{{ edu.institution }}{{ "}" }}{{ "{" }}{% if edu.gpa %}GPA: {{ edu.gpa }}{% endif %}{{ "}" }}
    {% endfor %}
  \resumeSubHeadingListEnd
{% endif %}

{% if work_experience %}
\section{Experience}
  \resumeSubHeadingListStart
    {% for exp in work_experience %}
    \resumeSubheading
      {{ "{" }}{{ exp.position }}{{ "}" }}{{ "{" }}{{ exp.duration }}{{ "}" }}
      {{ "{" }}{{ exp.company }}{{ "}" }}{{ "{" }}{{ "}" }}
      {% if exp.description %}
      \resumeItemListStart
        \resumeItem{{ "{" }}{{ exp.description }}{{ "}" }}
      \resumeItemListEnd
      {% endif %}
    {% endfor %}
  \resumeSubHeadingListEnd
{% endif %}

{% if projects %}
\section{Projects}
    \resumeSubHeadingListStart
      {% for project in projects %}
      \resumeProjectHeading
          {{ "{" }}\textbf{{ "{" }}{{ project.title }}{{ "}" }}{{ "}" }}{{ "{" }}{{ "}" }}
          {% if project.description %}
          \resumeItemListStart
            \resumeItem{{ "{" }}{{ project.description }}{{ "}" }}
          \resumeItemListEnd
          {% endif %}
      {% endfor %}
    \resumeSubHeadingListEnd
{% endif %}

{% if skills %}
\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Skills}{{ "{" }}: {{ skills|join(', ') }}
    }}
 \end{itemize}
{% endif %}

\end{document}
"""
    
    template = Template(latex_template)
    return template.render(**data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)