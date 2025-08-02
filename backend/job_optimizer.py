"""
Job Description Analysis and Resume Optimization Module

This module provides functionality to analyze job descriptions and optimize resumes
to better match job requirements using NLP techniques and AI.
"""

import re
import nltk
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class JobDescriptionOptimizer:
    def __init__(self):
        self.setup_nltk()
        self.setup_ai_models()
        
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            logger.info("Downloading NLTK data...")
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
    
    def setup_ai_models(self):
        """Initialize AI models for text analysis"""
        try:
            # Use a more suitable model for text analysis
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            self.classifier = pipeline("zero-shot-classification")
            logger.info("AI models loaded successfully")
        except Exception as e:
            logger.warning(f"AI models not available: {e}")
            self.summarizer = None
            self.classifier = None
    
    def extract_keywords(self, text, num_keywords=20):
        """Extract important keywords from job description"""
        # Clean and preprocess text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove common stopwords
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('english'))
        
        # Add job-specific stopwords
        job_stopwords = {
            'job', 'position', 'role', 'candidate', 'applicant', 'company', 
            'team', 'work', 'working', 'experience', 'required', 'preferred',
            'ability', 'skills', 'knowledge', 'opportunity', 'responsibilities'
        }
        stop_words.update(job_stopwords)
        
        # Tokenize and filter
        words = nltk.word_tokenize(text)
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Get POS tags to focus on nouns and adjectives
        pos_tags = nltk.pos_tag(words)
        keywords = [word for word, pos in pos_tags if pos.startswith(('NN', 'JJ', 'VB'))]
        
        # Count frequency
        keyword_freq = Counter(keywords)
        
        return dict(keyword_freq.most_common(num_keywords))
    
    def extract_skills(self, text):
        """Extract technical skills and competencies from job description"""
        # Common skill patterns
        skill_patterns = [
            r'\b(?:python|java|javascript|react|node\.?js|angular|vue|html|css|sql|mongodb|postgresql|mysql|docker|kubernetes|aws|azure|gcp|git|github|gitlab|jenkins|ci/cd|agile|scrum|machine learning|ai|data science|tensorflow|pytorch|pandas|numpy|sklearn|rest|api|microservices|devops|linux|windows|mac|ios|android|swift|kotlin|c\+\+|c#|php|ruby|go|rust|scala|r|matlab|tableau|power bi|excel|jira|confluence|slack|teams|zoom|figma|sketch|adobe|photoshop|illustrator|indesign|premiere|after effects|unity|unreal|blender|autocad|solidworks|salesforce|hubspot|mailchimp|google analytics|seo|sem|social media|marketing|content|copywriting|project management|leadership|communication|problem solving|analytical|creative|detail oriented|team player|self motivated|adaptable|innovative|strategic|customer focused|results driven)\b',
            r'\b(?:bachelor|master|phd|degree|certification|certified|license|licensed)\b.*?(?:computer science|engineering|business|marketing|design|data|analytics|statistics|mathematics|finance|accounting|economics|psychology|communications|english|journalism|liberal arts|science|technology|information systems|cybersecurity|network|database|cloud|mobile|web|frontend|backend|fullstack|devops|qa|testing|ui|ux|product|project|program|operations|sales|customer|support|hr|human resources|legal|compliance|finance|accounting|supply chain|logistics|manufacturing|healthcare|education|nonprofit|government|consulting|startup|enterprise)\b'
        ]
        
        skills = set()
        for pattern in skill_patterns:
            matches = re.findall(pattern, text.lower())
            skills.update(matches)
        
        # Extract years of experience
        exp_pattern = r'(\d+)[\+\-\s]*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        exp_matches = re.findall(exp_pattern, text.lower())
        if exp_matches:
            skills.add(f"{max(exp_matches)} years experience")
        
        return list(skills)
    
    def analyze_job_description(self, job_description):
        """Comprehensive analysis of job description"""
        analysis = {
            'keywords': self.extract_keywords(job_description),
            'skills': self.extract_skills(job_description),
            'requirements': self.extract_requirements(job_description),
            'job_level': self.determine_job_level(job_description),
            'industry': self.identify_industry(job_description)
        }
        
        # Add AI-powered analysis if available
        if self.summarizer and len(job_description) > 100:
            try:
                summary = self.summarizer(job_description, max_length=130, min_length=30, do_sample=False)
                analysis['summary'] = summary[0]['summary_text']
            except Exception as e:
                logger.warning(f"AI summarization failed: {e}")
                analysis['summary'] = job_description[:200] + "..."
        
        return analysis
    
    def extract_requirements(self, text):
        """Extract specific requirements from job description"""
        requirements = {
            'education': [],
            'experience': [],
            'technical': [],
            'soft_skills': []
        }
        
        # Education requirements
        edu_pattern = r'(?:bachelor|master|phd|degree|diploma|certification).*?(?:required|preferred|desired)'
        edu_matches = re.findall(edu_pattern, text.lower())
        requirements['education'] = edu_matches
        
        # Experience requirements
        exp_pattern = r'(\d+)[\+\-\s]*(?:years?|yrs?).*?(?:experience|exp)'
        exp_matches = re.findall(exp_pattern, text.lower())
        requirements['experience'] = [f"{exp}+ years" for exp in exp_matches]
        
        # Technical skills (already extracted in extract_skills)
        requirements['technical'] = self.extract_skills(text)
        
        # Soft skills
        soft_skills = ['leadership', 'communication', 'teamwork', 'problem solving', 
                      'analytical', 'creative', 'detail oriented', 'organized', 
                      'self motivated', 'adaptable', 'innovative', 'strategic']
        
        for skill in soft_skills:
            if skill in text.lower():
                requirements['soft_skills'].append(skill)
        
        return requirements
    
    def determine_job_level(self, text):
        """Determine job seniority level"""
        text_lower = text.lower()
        
        senior_indicators = ['senior', 'lead', 'principal', 'architect', 'manager', 'director', 'vp', 'chief']
        junior_indicators = ['junior', 'entry', 'associate', 'intern', 'trainee', 'graduate']
        mid_indicators = ['mid', 'intermediate', 'regular', 'standard']
        
        senior_count = sum(1 for indicator in senior_indicators if indicator in text_lower)
        junior_count = sum(1 for indicator in junior_indicators if indicator in text_lower)
        mid_count = sum(1 for indicator in mid_indicators if indicator in text_lower)
        
        if senior_count > junior_count and senior_count > mid_count:
            return 'Senior'
        elif junior_count > 0:
            return 'Junior'
        else:
            return 'Mid-Level'
    
    def identify_industry(self, text):
        """Identify industry/sector from job description"""
        industries = {
            'Technology': ['software', 'tech', 'it', 'computer', 'digital', 'startup', 'saas'],
            'Finance': ['finance', 'banking', 'investment', 'fintech', 'trading', 'insurance'],
            'Healthcare': ['healthcare', 'medical', 'hospital', 'pharmaceutical', 'biotech'],
            'Education': ['education', 'school', 'university', 'academic', 'teaching'],
            'Retail': ['retail', 'e-commerce', 'sales', 'customer', 'merchandise'],
            'Manufacturing': ['manufacturing', 'production', 'factory', 'industrial'],
            'Consulting': ['consulting', 'advisory', 'strategy', 'management'],
            'Marketing': ['marketing', 'advertising', 'brand', 'campaign', 'social media'],
            'Government': ['government', 'public', 'federal', 'state', 'municipal'],
            'Nonprofit': ['nonprofit', 'ngo', 'charity', 'foundation', 'social impact']
        }
        
        text_lower = text.lower()
        industry_scores = {}
        
        for industry, keywords in industries.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                industry_scores[industry] = score
        
        if industry_scores:
            return max(industry_scores, key=industry_scores.get)
        return 'General'
    
    def calculate_match_score(self, resume_data, job_analysis):
        """Calculate how well resume matches job requirements"""
        # Extract text from resume
        resume_text = self.extract_resume_text(resume_data)
        
        # Get keywords from both
        resume_keywords = self.extract_keywords(resume_text)
        job_keywords = job_analysis['keywords']
        
        # Calculate keyword overlap
        common_keywords = set(resume_keywords.keys()) & set(job_keywords.keys())
        keyword_score = len(common_keywords) / max(len(job_keywords), 1) * 100
        
        # Calculate skill match
        resume_skills = set([skill.lower() for skill in resume_data.get('skills', [])])
        job_skills = set([skill.lower() for skill in job_analysis['skills']])
        skill_overlap = len(resume_skills & job_skills)
        skill_score = skill_overlap / max(len(job_skills), 1) * 100
        
        # Overall match score
        overall_score = (keyword_score * 0.4 + skill_score * 0.6)
        
        return {
            'overall_score': round(overall_score, 1),
            'keyword_score': round(keyword_score, 1),
            'skill_score': round(skill_score, 1),
            'matched_keywords': list(common_keywords),
            'matched_skills': list(resume_skills & job_skills),
            'missing_skills': list(job_skills - resume_skills)
        }
    
    def extract_resume_text(self, resume_data):
        """Extract all text from resume data for analysis"""
        text_parts = []
        
        # Add work experience descriptions
        for exp in resume_data.get('work_experience', []):
            if exp.get('description'):
                text_parts.append(exp['description'])
        
        # Add project descriptions
        for project in resume_data.get('projects', []):
            if project.get('description'):
                text_parts.append(project['description'])
        
        # Add skills
        text_parts.extend(resume_data.get('skills', []))
        
        # Add education
        for edu in resume_data.get('education', []):
            text_parts.append(edu.get('degree', ''))
        
        return ' '.join(text_parts)
    
    def optimize_resume(self, resume_data, job_analysis):
        """Generate optimized resume suggestions based on job analysis"""
        match_score = self.calculate_match_score(resume_data, job_analysis)
        
        suggestions = {
            'skills_to_add': [],
            'keywords_to_include': [],
            'experience_improvements': [],
            'project_improvements': [],
            'overall_suggestions': []
        }
        
        # Skills suggestions
        missing_skills = match_score['missing_skills'][:5]  # Top 5 missing skills
        suggestions['skills_to_add'] = missing_skills
        
        # Keywords to include
        job_keywords = list(job_analysis['keywords'].keys())[:10]
        resume_text = self.extract_resume_text(resume_data).lower()
        missing_keywords = [kw for kw in job_keywords if kw not in resume_text][:5]
        suggestions['keywords_to_include'] = missing_keywords
        
        # Experience improvements
        for i, exp in enumerate(resume_data.get('work_experience', [])):
            if exp.get('description'):
                improved_desc = self.improve_description(
                    exp['description'], 
                    job_analysis['keywords'],
                    job_analysis['skills']
                )
                if improved_desc != exp['description']:
                    suggestions['experience_improvements'].append({
                        'index': i,
                        'original': exp['description'],
                        'improved': improved_desc
                    })
        
        # Project improvements
        for i, project in enumerate(resume_data.get('projects', [])):
            if project.get('description'):
                improved_desc = self.improve_description(
                    project['description'], 
                    job_analysis['keywords'],
                    job_analysis['skills']
                )
                if improved_desc != project['description']:
                    suggestions['project_improvements'].append({
                        'index': i,
                        'original': project['description'],
                        'improved': improved_desc
                    })
        
        # Overall suggestions based on match score
        if match_score['overall_score'] < 30:
            suggestions['overall_suggestions'].append(
                "Your resume has low compatibility with this job. Consider adding more relevant skills and experience."
            )
        elif match_score['overall_score'] < 60:
            suggestions['overall_suggestions'].append(
                "Your resume shows moderate compatibility. Focus on highlighting relevant experience and adding missing skills."
            )
        else:
            suggestions['overall_suggestions'].append(
                "Great match! Your resume aligns well with the job requirements."
            )
        
        # Add specific suggestions based on job level
        job_level = job_analysis.get('job_level', 'Mid-Level')
        if job_level == 'Senior' and match_score['overall_score'] < 70:
            suggestions['overall_suggestions'].append(
                "For senior roles, emphasize leadership experience and strategic impact in your descriptions."
            )
        
        return {
            'match_score': match_score,
            'suggestions': suggestions,
            'job_analysis': job_analysis
        }
    
    def improve_description(self, description, job_keywords, job_skills):
        """Improve a description by incorporating relevant keywords and skills"""
        if not description:
            return description
        
        # Simple keyword incorporation (can be enhanced with AI)
        improved = description
        description_lower = description.lower()
        
        # Add relevant keywords that are missing
        relevant_keywords = []
        for keyword in list(job_keywords.keys())[:3]:  # Top 3 keywords
            if keyword not in description_lower and len(keyword) > 3:
                relevant_keywords.append(keyword)
        
        # Add relevant skills that are missing
        relevant_skills = []
        for skill in job_skills[:2]:  # Top 2 skills
            if skill.lower() not in description_lower:
                relevant_skills.append(skill)
        
        # Enhance with action words
        action_words = ['developed', 'implemented', 'managed', 'led', 'created', 'optimized', 'improved', 'designed']
        if not any(word in description_lower for word in action_words):
            if not description.startswith(tuple(action_words)):
                improved = f"Developed and {description.lower()}"
        
        return improved