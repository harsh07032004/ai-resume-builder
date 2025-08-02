# AI-Powered Resume Generator

A full-stack web application that generates professional resumes using AI-enhanced descriptions and LaTeX templates.

## Features

### Frontend (React + Tailwind CSS)
- 🎨 **Modern, responsive UI** with dark/light mode toggle
- 📝 **Multi-section form** for comprehensive resume data:
  - Personal information (name, email, phone, LinkedIn)
  - Education (multiple entries with degree, institution, year, GPA)
  - Work experience (multiple entries with AI enhancement option)
  - Projects (title and description with AI enhancement)
  - Skills (comma-separated tags)
- 🎯 **Job-Tailored Optimization** - NEW FEATURE!
  - Paste job descriptions to get personalized optimization
  - AI-powered job analysis (skills, keywords, requirements)
  - Resume match scoring with detailed breakdown
  - Specific improvement suggestions for experience and projects
  - One-click application of selected improvements
- 👁️ **Live preview** of generated resume
- 📱 **Mobile-responsive** design
- ⚡ **AI enhancement toggle** for improving descriptions

### Backend (Flask + Python)
- 🚀 **RESTful API** with Flask
- 🤖 **AI text enhancement** using HuggingFace Transformers (T5-small)
- 🎯 **Job Description Analysis** - NEW!
  - NLP-powered keyword extraction and skill identification
  - Industry and seniority level detection
  - Resume-to-job matching algorithms
  - Intelligent improvement suggestions
- 📄 **LaTeX template engine** with Jinja2
- 🔄 **PDF generation** using pdflatex
- 🌐 **CORS enabled** for frontend integration

### AI Enhancement
- Uses T5-small model to improve work experience and project descriptions
- Optional feature that can be toggled on/off
- Enhances professional language and impact of descriptions

## Tech Stack

- **Frontend**: React 18, Tailwind CSS, Axios, React Icons
- **Backend**: Flask, Jinja2, HuggingFace Transformers, PyTorch
- **PDF Generation**: LaTeX (pdflatex)
- **AI Model**: T5-small for text enhancement

## Installation & Setup

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- LaTeX distribution (texlive)

### Backend Setup

1. **Install LaTeX** (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

2. **Install Python dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

3. **Run the Flask server**:
```bash
python app.py
```
The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Start the development server**:
```bash
npm start
```
The frontend will run on `http://localhost:3000`

## API Endpoints

### Core Resume Endpoints

### `POST /generate`
Generates and returns a PDF resume.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1 (555) 123-4567",
  "linkedin": "https://linkedin.com/in/johndoe",
  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "University of Technology",
      "year": "2020-2024",
      "gpa": "3.8/4.0"
    }
  ],
  "work_experience": [
    {
      "position": "Software Engineer",
      "company": "Tech Corp",
      "duration": "Jan 2022 - Present",
      "description": "Developed web applications using React and Node.js"
    }
  ],
  "projects": [
    {
      "title": "E-commerce Website",
      "description": "Built a full-stack e-commerce platform"
    }
  ],
  "skills": ["JavaScript", "React", "Node.js", "Python"],
  "enhance_with_ai": true
}
```

**Response:** PDF file download

### `POST /preview`
Returns HTML preview of the resume.

**Request Body:** Same as `/generate`

**Response:**
```json
{
  "html": "<div>...</div>"
}
```

### Job Optimization Endpoints - NEW!

### `POST /analyze-job`
Analyzes a job description to extract requirements and keywords.

**Request Body:**
```json
{
  "job_description": "We are seeking a Senior Software Engineer with 5+ years experience in React, Node.js, and Python..."
}
```

**Response:**
```json
{
  "analysis": {
    "job_level": "Senior",
    "industry": "Technology",
    "skills": ["react", "node.js", "python", "javascript"],
    "keywords": {"engineer": 3, "development": 2, "experience": 4},
    "requirements": {
      "education": ["bachelor degree computer science"],
      "experience": ["5+ years"],
      "technical": ["react", "node.js", "python"],
      "soft_skills": ["leadership", "communication"]
    }
  }
}
```

### `POST /optimize-resume`
Optimizes resume based on job description analysis.

**Request Body:**
```json
{
  "resume_data": { /* resume data object */ },
  "job_description": "Job posting text..."
}
```

**Response:**
```json
{
  "optimization": {
    "match_score": {
      "overall_score": 75.5,
      "keyword_score": 80.0,
      "skill_score": 71.0,
      "matched_skills": ["javascript", "react"],
      "missing_skills": ["python", "docker"]
    },
    "suggestions": {
      "skills_to_add": ["Python", "Docker", "AWS"],
      "experience_improvements": [
        {
          "index": 0,
          "original": "Built web apps",
          "improved": "Developed scalable web applications using React and Node.js"
        }
      ],
      "overall_suggestions": ["Add more relevant technical skills", "Highlight leadership experience"]
    }
  }
}
```

### `POST /apply-suggestions`
Applies selected optimization suggestions to resume data.

**Request Body:**
```json
{
  "resume_data": { /* original resume */ },
  "suggestions": { /* optimization suggestions */ },
  "selected_improvements": [
    {
      "type": "experience",
      "index": 0,
      "improved": "Enhanced description..."
    }
  ],
  "add_suggested_skills": true
}
```

**Response:**
```json
{
  "optimized_resume": { /* updated resume data */ }
}
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "ai_enabled": true,
  "optimizer_enabled": true
}
```

## Usage

### Basic Resume Creation
1. **Fill out the form** with your resume information
2. **Toggle AI enhancement** if you want improved descriptions
3. **Click "Preview Resume"** to see how it looks
4. **Click "Download PDF"** to generate and download your resume

### Job-Tailored Optimization - NEW!
1. **Switch to the "Job Optimizer" tab**
2. **Paste a job description** from the job posting you're applying to
3. **Click "Analyze Job"** to see extracted requirements and keywords
4. **Click "Optimize Resume"** to get personalized suggestions and match score
5. **Review suggestions** for experience improvements, missing skills, and keywords
6. **Select improvements** you want to apply using checkboxes
7. **Click "Apply Selected Improvements"** to automatically update your resume
8. **Generate your optimized resume** tailored to the specific job

## Project Structure

```
/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── generated/          # Generated PDF files
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResumeForm.js      # Main form component
│   │   │   ├── ResumePreview.js   # Preview component
│   │   │   └── ThemeToggle.js     # Dark/light mode toggle
│   │   ├── App.js          # Main React component
│   │   └── index.css       # Tailwind CSS imports
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind configuration
└── README.md
```

## Features in Detail

### AI Text Enhancement
- Uses the T5-small model from HuggingFace
- Improves work experience and project descriptions
- Makes language more professional and impactful
- Optional feature that can be disabled

### LaTeX Template
- Professional, clean resume layout
- ATS-friendly format
- Customizable sections
- Proper typography and spacing

### Responsive Design
- Works on desktop, tablet, and mobile
- Dark/light mode support
- Intuitive user interface
- Real-time form validation

## Troubleshooting

### LaTeX Installation Issues
If you encounter LaTeX compilation errors:
1. Ensure all LaTeX packages are installed
2. Check that `pdflatex` is in your PATH
3. Verify write permissions in the backend directory

### AI Model Loading
If the AI enhancement fails:
1. Check internet connection (model downloads on first use)
2. Ensure sufficient memory (T5-small requires ~250MB)
3. AI features will gracefully degrade if unavailable

### CORS Issues
If frontend can't reach backend:
1. Ensure backend is running on port 5000
2. Check that CORS is properly configured
3. Verify no firewall blocking the connection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
