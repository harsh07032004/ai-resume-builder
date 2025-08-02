#!/usr/bin/env python3
"""
Test script for the Job Description Optimization feature.
"""

import requests
import json

# Sample job description
SAMPLE_JOB_DESCRIPTION = """
Senior Software Engineer - Full Stack

We are seeking a highly skilled Senior Software Engineer to join our dynamic team. The ideal candidate will have 5+ years of experience in full-stack development with expertise in React, Node.js, and Python.

Key Responsibilities:
- Design and develop scalable web applications using React and Node.js
- Build robust backend services with Python and FastAPI
- Work with PostgreSQL databases and implement efficient data models
- Collaborate with cross-functional teams in an Agile environment
- Mentor junior developers and contribute to code reviews
- Implement CI/CD pipelines using Docker and Kubernetes
- Ensure code quality through unit testing and integration testing

Required Qualifications:
- Bachelor's degree in Computer Science or related field
- 5+ years of professional software development experience
- Strong proficiency in JavaScript, React, and Node.js
- Experience with Python and web frameworks (Django/FastAPI)
- Knowledge of SQL databases, preferably PostgreSQL
- Familiarity with cloud platforms (AWS, Azure, or GCP)
- Experience with version control systems (Git)
- Strong problem-solving skills and attention to detail

Preferred Qualifications:
- Experience with Docker and container orchestration
- Knowledge of microservices architecture
- Familiarity with DevOps practices and CI/CD
- Experience with machine learning or data science
- Leadership or mentoring experience

We offer competitive salary, comprehensive benefits, and opportunities for professional growth in a collaborative environment.
"""

# Sample resume data
SAMPLE_RESUME_DATA = {
    "name": "Alex Johnson",
    "email": "alex.johnson@email.com",
    "phone": "+1 (555) 987-6543",
    "linkedin": "https://linkedin.com/in/alexjohnson",
    "education": [
        {
            "degree": "Bachelor of Science in Computer Science",
            "institution": "State University",
            "year": "2018-2022",
            "gpa": "3.7/4.0"
        }
    ],
    "work_experience": [
        {
            "position": "Software Developer",
            "company": "Tech Solutions Inc",
            "duration": "June 2022 - Present",
            "description": "Developed web applications using JavaScript and React. Worked on backend services with Node.js and databases."
        },
        {
            "position": "Junior Developer",
            "company": "StartupCorp",
            "duration": "Jan 2021 - May 2022",
            "description": "Built frontend components and helped with testing. Used HTML, CSS, and basic JavaScript."
        }
    ],
    "projects": [
        {
            "title": "E-commerce Platform",
            "description": "Created an online shopping website with React frontend and Express.js backend. Used MongoDB for data storage."
        },
        {
            "title": "Task Management App",
            "description": "Built a todo application with user authentication and real-time updates using WebSocket."
        }
    ],
    "skills": ["JavaScript", "React", "Node.js", "HTML", "CSS", "MongoDB", "Git"],
    "enhance_with_ai": False
}

def test_job_analysis():
    """Test job description analysis endpoint"""
    print("🔍 Testing Job Description Analysis...")
    
    try:
        response = requests.post("http://localhost:5000/analyze-job", json={
            "job_description": SAMPLE_JOB_DESCRIPTION
        })
        
        if response.status_code == 200:
            data = response.json()
            analysis = data['analysis']
            
            print("✅ Job analysis successful!")
            print(f"   Job Level: {analysis.get('job_level', 'N/A')}")
            print(f"   Industry: {analysis.get('industry', 'N/A')}")
            print(f"   Skills Found: {len(analysis.get('skills', []))}")
            print(f"   Keywords Found: {len(analysis.get('keywords', {}))}")
            
            # Show top skills and keywords
            if analysis.get('skills'):
                print(f"   Top Skills: {', '.join(analysis['skills'][:5])}")
            
            if analysis.get('keywords'):
                top_keywords = list(analysis['keywords'].keys())[:5]
                print(f"   Top Keywords: {', '.join(top_keywords)}")
            
            return True
        else:
            print(f"❌ Job analysis failed - status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Job analysis error: {e}")
        return False

def test_resume_optimization():
    """Test resume optimization endpoint"""
    print("\n🎯 Testing Resume Optimization...")
    
    try:
        response = requests.post("http://localhost:5000/optimize-resume", json={
            "resume_data": SAMPLE_RESUME_DATA,
            "job_description": SAMPLE_JOB_DESCRIPTION
        })
        
        if response.status_code == 200:
            data = response.json()
            optimization = data['optimization']
            match_score = optimization['match_score']
            suggestions = optimization['suggestions']
            
            print("✅ Resume optimization successful!")
            print(f"   Overall Match Score: {match_score['overall_score']}%")
            print(f"   Keyword Match: {match_score['keyword_score']}%")
            print(f"   Skill Match: {match_score['skill_score']}%")
            
            print(f"   Matched Skills: {len(match_score.get('matched_skills', []))}")
            print(f"   Missing Skills: {len(match_score.get('missing_skills', []))}")
            
            if match_score.get('matched_skills'):
                print(f"   Your Skills: {', '.join(match_score['matched_skills'][:3])}")
            
            if match_score.get('missing_skills'):
                print(f"   Suggested Skills: {', '.join(match_score['missing_skills'][:3])}")
            
            # Show suggestions
            if suggestions.get('skills_to_add'):
                print(f"   Skills to Add: {len(suggestions['skills_to_add'])}")
            
            if suggestions.get('experience_improvements'):
                print(f"   Experience Improvements: {len(suggestions['experience_improvements'])}")
            
            if suggestions.get('project_improvements'):
                print(f"   Project Improvements: {len(suggestions['project_improvements'])}")
            
            if suggestions.get('overall_suggestions'):
                print("   Recommendations:")
                for suggestion in suggestions['overall_suggestions']:
                    print(f"     • {suggestion}")
            
            return optimization
        else:
            print(f"❌ Resume optimization failed - status {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Resume optimization error: {e}")
        return None

def test_apply_suggestions():
    """Test applying suggestions endpoint"""
    print("\n✨ Testing Apply Suggestions...")
    
    # First get optimization results
    optimization = test_resume_optimization()
    if not optimization:
        print("❌ Cannot test apply suggestions without optimization results")
        return False
    
    # Create sample improvements to apply
    selected_improvements = []
    suggestions = optimization['suggestions']
    
    # Add experience improvements if available
    if suggestions.get('experience_improvements'):
        for i, improvement in enumerate(suggestions['experience_improvements'][:1]):  # Apply first one
            selected_improvements.append({
                'id': f'experience-{improvement["index"]}',
                'type': 'experience',
                'index': improvement['index'],
                'improved': improvement['improved']
            })
    
    # Add project improvements if available
    if suggestions.get('project_improvements'):
        for i, improvement in enumerate(suggestions['project_improvements'][:1]):  # Apply first one
            selected_improvements.append({
                'id': f'project-{improvement["index"]}',
                'type': 'project', 
                'index': improvement['index'],
                'improved': improvement['improved']
            })
    
    if not selected_improvements:
        print("ℹ️  No improvements to apply")
        return True
    
    try:
        response = requests.post("http://localhost:5000/apply-suggestions", json={
            "resume_data": SAMPLE_RESUME_DATA,
            "suggestions": suggestions,
            "selected_improvements": selected_improvements,
            "add_suggested_skills": True
        })
        
        if response.status_code == 200:
            data = response.json()
            optimized_resume = data['optimized_resume']
            
            print("✅ Suggestions applied successfully!")
            print(f"   Original Skills: {len(SAMPLE_RESUME_DATA['skills'])}")
            print(f"   Optimized Skills: {len(optimized_resume['skills'])}")
            
            # Show new skills added
            original_skills = set(SAMPLE_RESUME_DATA['skills'])
            new_skills = set(optimized_resume['skills']) - original_skills
            if new_skills:
                print(f"   Added Skills: {', '.join(list(new_skills)[:3])}")
            
            print(f"   Improvements Applied: {len(selected_improvements)}")
            return True
        else:
            print(f"❌ Apply suggestions failed - status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Apply suggestions error: {e}")
        return False

def test_health_check():
    """Test health check with optimizer status"""
    print("🏥 Testing Health Check...")
    
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   AI Enabled: {data.get('ai_enabled')}")
            print(f"   Optimizer Enabled: {data.get('optimizer_enabled')}")
            return True
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def main():
    """Run all job optimizer tests"""
    print("🧪 Testing AI Resume Generator - Job Optimization Features\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Job Description Analysis", test_job_analysis),
        ("Resume Optimization", lambda: test_resume_optimization() is not None),
        ("Apply Suggestions", test_apply_suggestions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All job optimization tests passed! The feature is working correctly.")
        print("\n💡 How to use the Job Optimizer:")
        print("   1. Go to the 'Job Optimizer' tab in the web interface")
        print("   2. Paste a job description in the text area")
        print("   3. Click 'Analyze Job' to see job requirements")
        print("   4. Click 'Optimize Resume' to get personalized suggestions")
        print("   5. Select improvements you want to apply")
        print("   6. Click 'Apply Selected Improvements' to update your resume")
    else:
        print("⚠️  Some tests failed. Check the backend server and dependencies.")

if __name__ == "__main__":
    main()