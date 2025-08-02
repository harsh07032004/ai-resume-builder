import React, { useState } from 'react';
import { FiTarget, FiTrendingUp, FiCheckCircle, FiAlertCircle, FiRefreshCw, FiEye } from 'react-icons/fi';
import axios from 'axios';

const JobOptimizer = ({ formData, onChange, darkMode }) => {
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [optimization, setOptimization] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedImprovements, setSelectedImprovements] = useState([]);

  const inputClass = `w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
    darkMode 
      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
      : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
  }`;

  const buttonClass = (variant = 'primary') => {
    const baseClass = 'flex items-center justify-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors disabled:cursor-not-allowed';
    
    if (variant === 'secondary') {
      return `${baseClass} ${
        darkMode 
          ? 'bg-gray-600 hover:bg-gray-700 disabled:bg-gray-700 text-white' 
          : 'bg-gray-200 hover:bg-gray-300 disabled:bg-gray-300 text-gray-700'
      }`;
    }
    
    return `${baseClass} ${
      darkMode 
        ? 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white' 
        : 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white'
    }`;
  };

  const analyzeJobDescription = async () => {
    if (!jobDescription.trim()) {
      alert('Please enter a job description');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await axios.post('http://localhost:5000/analyze-job', {
        job_description: jobDescription
      });
      
      setAnalysis(response.data.analysis);
    } catch (error) {
      console.error('Error analyzing job description:', error);
      alert('Failed to analyze job description. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const optimizeResume = async () => {
    if (!jobDescription.trim()) {
      alert('Please enter and analyze a job description first');
      return;
    }

    if (!formData.name || !formData.email) {
      alert('Please fill in your name and email first');
      return;
    }

    setIsOptimizing(true);
    try {
      const response = await axios.post('http://localhost:5000/optimize-resume', {
        resume_data: formData,
        job_description: jobDescription
      });
      
      setOptimization(response.data.optimization);
      setShowSuggestions(true);
    } catch (error) {
      console.error('Error optimizing resume:', error);
      alert('Failed to optimize resume. Please try again.');
    } finally {
      setIsOptimizing(false);
    }
  };

  const toggleImprovement = (type, index, improvement) => {
    const improvementId = `${type}-${index}`;
    const existing = selectedImprovements.find(imp => imp.id === improvementId);
    
    if (existing) {
      setSelectedImprovements(prev => prev.filter(imp => imp.id !== improvementId));
    } else {
      setSelectedImprovements(prev => [...prev, {
        id: improvementId,
        type,
        index,
        improved: improvement.improved
      }]);
    }
  };

  const applySelectedImprovements = async () => {
    if (selectedImprovements.length === 0) {
      alert('Please select at least one improvement to apply');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/apply-suggestions', {
        resume_data: formData,
        suggestions: optimization.suggestions,
        selected_improvements: selectedImprovements,
        add_suggested_skills: true // You can make this configurable
      });
      
      // Update the form data with optimized resume
      onChange(response.data.optimized_resume);
      
      // Reset selections
      setSelectedImprovements([]);
      alert('Improvements applied successfully!');
    } catch (error) {
      console.error('Error applying improvements:', error);
      alert('Failed to apply improvements. Please try again.');
    }
  };

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
      <div className="flex items-center space-x-3 mb-6">
        <FiTarget className={`text-2xl ${darkMode ? 'text-blue-400' : 'text-blue-600'}`} />
        <h2 className={`text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
          Job-Tailored Optimization
        </h2>
      </div>

      {/* Job Description Input */}
      <div className="mb-6">
        <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
          Job Description
        </label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the job description here to optimize your resume for this specific role..."
          rows={6}
          className={inputClass}
        />
        <p className={`text-xs mt-2 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
          Copy and paste the complete job posting to get personalized optimization suggestions.
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <button
          onClick={analyzeJobDescription}
          disabled={isAnalyzing || !jobDescription.trim()}
          className={buttonClass('secondary')}
        >
          {isAnalyzing ? <FiRefreshCw className="animate-spin" /> : <FiEye />}
          <span>{isAnalyzing ? 'Analyzing...' : 'Analyze Job'}</span>
        </button>
        
        <button
          onClick={optimizeResume}
          disabled={isOptimizing || !jobDescription.trim() || !formData.name}
          className={buttonClass()}
        >
          {isOptimizing ? <FiRefreshCw className="animate-spin" /> : <FiTrendingUp />}
          <span>{isOptimizing ? 'Optimizing...' : 'Optimize Resume'}</span>
        </button>
      </div>

      {/* Job Analysis Results */}
      {analysis && (
        <div className={`mb-6 p-4 rounded-lg border ${darkMode ? 'border-gray-600 bg-gray-700' : 'border-gray-200 bg-gray-50'}`}>
          <h3 className={`text-lg font-semibold mb-3 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
            Job Analysis
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <p className={`text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                Job Level: <span className={`${darkMode ? 'text-blue-400' : 'text-blue-600'}`}>{analysis.job_level}</span>
              </p>
              <p className={`text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                Industry: <span className={`${darkMode ? 'text-blue-400' : 'text-blue-600'}`}>{analysis.industry}</span>
              </p>
            </div>
          </div>

          {analysis.skills && analysis.skills.length > 0 && (
            <div className="mb-4">
              <h4 className={`text-sm font-semibold mb-2 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                Required Skills ({analysis.skills.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {analysis.skills.slice(0, 10).map((skill, index) => (
                  <span
                    key={index}
                    className={`px-2 py-1 rounded text-xs ${
                      darkMode 
                        ? 'bg-purple-600 text-white' 
                        : 'bg-purple-100 text-purple-800'
                    }`}
                  >
                    {skill}
                  </span>
                ))}
                {analysis.skills.length > 10 && (
                  <span className={`px-2 py-1 rounded text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                    +{analysis.skills.length - 10} more
                  </span>
                )}
              </div>
            </div>
          )}

          {analysis.keywords && Object.keys(analysis.keywords).length > 0 && (
            <div>
              <h4 className={`text-sm font-semibold mb-2 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                Key Terms
              </h4>
              <div className="flex flex-wrap gap-2">
                {Object.entries(analysis.keywords).slice(0, 8).map(([keyword, freq], index) => (
                  <span
                    key={index}
                    className={`px-2 py-1 rounded text-xs ${
                      darkMode 
                        ? 'bg-green-600 text-white' 
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {keyword} ({freq})
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Optimization Results */}
      {optimization && showSuggestions && (
        <div className={`p-4 rounded-lg border ${darkMode ? 'border-gray-600 bg-gray-700' : 'border-gray-200 bg-gray-50'}`}>
          <h3 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
            Optimization Results
          </h3>

          {/* Match Score */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <span className={`font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                Overall Match Score
              </span>
              <span className={`text-2xl font-bold ${getScoreColor(optimization.match_score.overall_score)}`}>
                {optimization.match_score.overall_score}%
              </span>
            </div>
            <div className={`w-full bg-gray-200 rounded-full h-2 ${darkMode ? 'bg-gray-600' : ''}`}>
              <div
                className={`h-2 rounded-full ${
                  optimization.match_score.overall_score >= 70 ? 'bg-green-600' :
                  optimization.match_score.overall_score >= 40 ? 'bg-yellow-600' : 'bg-red-600'
                }`}
                style={{ width: `${optimization.match_score.overall_score}%` }}
              ></div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 mt-3 text-sm">
              <div>
                <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>
                  Keyword Match: <span className={`font-medium ${getScoreColor(optimization.match_score.keyword_score)}`}>
                    {optimization.match_score.keyword_score}%
                  </span>
                </span>
              </div>
              <div>
                <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>
                  Skill Match: <span className={`font-medium ${getScoreColor(optimization.match_score.skill_score)}`}>
                    {optimization.match_score.skill_score}%
                  </span>
                </span>
              </div>
            </div>
          </div>

          {/* Suggestions */}
          {optimization.suggestions.overall_suggestions.length > 0 && (
            <div className="mb-4">
              <h4 className={`text-sm font-semibold mb-2 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                Recommendations
              </h4>
              {optimization.suggestions.overall_suggestions.map((suggestion, index) => (
                <div key={index} className={`flex items-start space-x-2 mb-2`}>
                  <FiAlertCircle className={`text-sm mt-0.5 ${darkMode ? 'text-yellow-400' : 'text-yellow-600'}`} />
                  <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                    {suggestion}
                  </p>
                </div>
              ))}
            </div>
          )}

          {/* Skills to Add */}
          {optimization.suggestions.skills_to_add.length > 0 && (
            <div className="mb-4">
              <h4 className={`text-sm font-semibold mb-2 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                Suggested Skills to Add
              </h4>
              <div className="flex flex-wrap gap-2">
                {optimization.suggestions.skills_to_add.map((skill, index) => (
                  <span
                    key={index}
                    className={`px-2 py-1 rounded text-xs ${
                      darkMode 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-blue-100 text-blue-800'
                    }`}
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Experience Improvements */}
          {optimization.suggestions.experience_improvements.length > 0 && (
            <div className="mb-4">
              <h4 className={`text-sm font-semibold mb-3 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                Experience Improvements
              </h4>
              {optimization.suggestions.experience_improvements.map((improvement, index) => (
                <div key={index} className={`mb-4 p-3 rounded border ${darkMode ? 'border-gray-600' : 'border-gray-200'}`}>
                  <div className="flex items-start justify-between mb-2">
                    <span className={`text-sm font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                      Experience #{improvement.index + 1}
                    </span>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={selectedImprovements.some(imp => imp.id === `experience-${improvement.index}`)}
                        onChange={() => toggleImprovement('experience', improvement.index, improvement)}
                        className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                      />
                      <span className={`text-xs ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>Apply</span>
                    </label>
                  </div>
                  <div className="space-y-2">
                    <div>
                      <p className={`text-xs font-medium ${darkMode ? 'text-red-400' : 'text-red-600'}`}>Original:</p>
                      <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                        {improvement.original}
                      </p>
                    </div>
                    <div>
                      <p className={`text-xs font-medium ${darkMode ? 'text-green-400' : 'text-green-600'}`}>Improved:</p>
                      <p className={`text-sm ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                        {improvement.improved}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Project Improvements */}
          {optimization.suggestions.project_improvements.length > 0 && (
            <div className="mb-4">
              <h4 className={`text-sm font-semibold mb-3 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                Project Improvements
              </h4>
              {optimization.suggestions.project_improvements.map((improvement, index) => (
                <div key={index} className={`mb-4 p-3 rounded border ${darkMode ? 'border-gray-600' : 'border-gray-200'}`}>
                  <div className="flex items-start justify-between mb-2">
                    <span className={`text-sm font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                      Project #{improvement.index + 1}
                    </span>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={selectedImprovements.some(imp => imp.id === `project-${improvement.index}`)}
                        onChange={() => toggleImprovement('project', improvement.index, improvement)}
                        className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                      />
                      <span className={`text-xs ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>Apply</span>
                    </label>
                  </div>
                  <div className="space-y-2">
                    <div>
                      <p className={`text-xs font-medium ${darkMode ? 'text-red-400' : 'text-red-600'}`}>Original:</p>
                      <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                        {improvement.original}
                      </p>
                    </div>
                    <div>
                      <p className={`text-xs font-medium ${darkMode ? 'text-green-400' : 'text-green-600'}`}>Improved:</p>
                      <p className={`text-sm ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                        {improvement.improved}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Apply Button */}
          {(optimization.suggestions.experience_improvements.length > 0 || 
            optimization.suggestions.project_improvements.length > 0) && (
            <div className="flex justify-end">
              <button
                onClick={applySelectedImprovements}
                disabled={selectedImprovements.length === 0}
                className={buttonClass()}
              >
                <FiCheckCircle />
                <span>Apply Selected Improvements ({selectedImprovements.length})</span>
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default JobOptimizer;