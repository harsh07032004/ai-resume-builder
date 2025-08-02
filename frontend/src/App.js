import React, { useState } from 'react';
import ResumeForm from './components/ResumeForm';
import ResumePreview from './components/ResumePreview';
import ThemeToggle from './components/ThemeToggle';
import { FiFileText, FiDownload } from 'react-icons/fi';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    linkedin: '',
    education: [{ degree: '', institution: '', year: '', gpa: '' }],
    work_experience: [{ position: '', company: '', duration: '', description: '' }],
    projects: [{ title: '', description: '' }],
    skills: [],
    enhance_with_ai: false
  });
  
  const [previewHtml, setPreviewHtml] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const handleFormChange = (newData) => {
    setFormData(newData);
  };

  const handlePreview = async () => {
    try {
      setIsGenerating(true);
      const response = await axios.post('http://localhost:5000/preview', formData);
      setPreviewHtml(response.data.html);
      setShowPreview(true);
    } catch (error) {
      console.error('Error generating preview:', error);
      alert('Failed to generate preview. Make sure the backend is running.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      setIsGenerating(true);
      const response = await axios.post('http://localhost:5000/generate', formData, {
        responseType: 'blob'
      });
      
      // Create blob and download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${formData.name.replace(' ', '_')}_resume.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Failed to generate PDF. Make sure the backend is running and LaTeX is installed.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${
      darkMode ? 'dark bg-gray-900' : 'bg-gray-50'
    }`}>
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center space-x-3">
            <FiFileText className={`text-3xl ${darkMode ? 'text-blue-400' : 'text-blue-600'}`} />
            <h1 className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
              AI Resume Generator
            </h1>
          </div>
          <ThemeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
            <h2 className={`text-xl font-semibold mb-6 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
              Resume Information
            </h2>
            <ResumeForm 
              formData={formData} 
              onChange={handleFormChange}
              darkMode={darkMode}
            />
            
            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 mt-8">
              <button
                onClick={handlePreview}
                disabled={isGenerating || !formData.name || !formData.email}
                className={`flex items-center justify-center space-x-2 px-6 py-3 rounded-lg font-medium transition-colors ${
                  darkMode 
                    ? 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600' 
                    : 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400'
                } text-white disabled:cursor-not-allowed`}
              >
                <FiFileText />
                <span>{isGenerating ? 'Generating...' : 'Preview Resume'}</span>
              </button>
              
              <button
                onClick={handleDownloadPDF}
                disabled={isGenerating || !formData.name || !formData.email}
                className={`flex items-center justify-center space-x-2 px-6 py-3 rounded-lg font-medium transition-colors ${
                  darkMode 
                    ? 'bg-green-600 hover:bg-green-700 disabled:bg-gray-600' 
                    : 'bg-green-600 hover:bg-green-700 disabled:bg-gray-400'
                } text-white disabled:cursor-not-allowed`}
              >
                <FiDownload />
                <span>{isGenerating ? 'Generating...' : 'Download PDF'}</span>
              </button>
            </div>
          </div>

          {/* Preview Section */}
          <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-lg p-6`}>
            <h2 className={`text-xl font-semibold mb-6 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
              Preview
            </h2>
            {showPreview && previewHtml ? (
              <ResumePreview html={previewHtml} darkMode={darkMode} />
            ) : (
              <div className={`text-center py-12 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                <FiFileText className="text-6xl mx-auto mb-4 opacity-50" />
                <p>Click "Preview Resume" to see your resume here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
