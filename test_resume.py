#!/usr/bin/env python3
"""
Simple test script to verify the AI Resume Generator backend works correctly.
"""

import requests
import json

# Test data
test_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
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
            "description": "Developed web applications using React and Node.js. Built scalable microservices and improved system performance."
        }
    ],
    "projects": [
        {
            "title": "E-commerce Website",
            "description": "Built a full-stack e-commerce platform with React frontend and Node.js backend. Implemented payment processing and user authentication."
        }
    ],
    "skills": ["JavaScript", "React", "Node.js", "Python", "SQL", "Git"],
    "enhance_with_ai": False
}

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   AI Enabled: {data.get('ai_enabled')}")
            return True
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_preview_endpoint():
    """Test the preview endpoint"""
    try:
        response = requests.post("http://localhost:5000/preview", json=test_data)
        if response.status_code == 200:
            data = response.json()
            if 'html' in data and data['html']:
                print("✅ Preview generation passed")
                print(f"   HTML length: {len(data['html'])} characters")
                return True
            else:
                print("❌ Preview generation failed - no HTML returned")
                return False
        else:
            print(f"❌ Preview generation failed - status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Preview generation error: {e}")
        return False

def test_pdf_generation():
    """Test PDF generation endpoint"""
    try:
        response = requests.post("http://localhost:5000/generate", json=test_data)
        if response.status_code == 200:
            if response.headers.get('content-type') == 'application/pdf':
                print("✅ PDF generation passed")
                print(f"   PDF size: {len(response.content)} bytes")
                # Save the PDF for manual inspection
                with open('test_resume.pdf', 'wb') as f:
                    f.write(response.content)
                print("   PDF saved as 'test_resume.pdf'")
                return True
            else:
                print("❌ PDF generation failed - wrong content type")
                return False
        else:
            print(f"❌ PDF generation failed - status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ PDF generation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing AI Resume Generator Backend\n")
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Preview Generation", test_preview_endpoint),
        ("PDF Generation", test_pdf_generation)
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
        print("🎉 All tests passed! The AI Resume Generator is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the backend server and dependencies.")

if __name__ == "__main__":
    main()