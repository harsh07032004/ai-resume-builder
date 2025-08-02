import React from 'react';
import { FiPlus, FiTrash2, FiZap } from 'react-icons/fi';

const ResumeForm = ({ formData, onChange, darkMode }) => {
  const updateField = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  const updateArrayField = (field, index, key, value) => {
    const newArray = [...formData[field]];
    newArray[index] = { ...newArray[index], [key]: value };
    onChange({ ...formData, [field]: newArray });
  };

  const addArrayItem = (field, template) => {
    const newArray = [...formData[field], template];
    onChange({ ...formData, [field]: newArray });
  };

  const removeArrayItem = (field, index) => {
    const newArray = formData[field].filter((_, i) => i !== index);
    onChange({ ...formData, [field]: newArray });
  };

  const handleSkillsChange = (value) => {
    const skills = value.split(',').map(skill => skill.trim()).filter(skill => skill);
    updateField('skills', skills);
  };

  const inputClass = `w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
    darkMode 
      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
      : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
  }`;

  const labelClass = `block text-sm font-medium mb-2 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`;

  return (
    <div className="space-y-6">
      {/* Personal Information */}
      <div>
        <h3 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
          Personal Information
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className={labelClass}>Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => updateField('name', e.target.value)}
              placeholder="John Doe"
              className={inputClass}
              required
            />
          </div>
          <div>
            <label className={labelClass}>Email *</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => updateField('email', e.target.value)}
              placeholder="john.doe@email.com"
              className={inputClass}
              required
            />
          </div>
          <div>
            <label className={labelClass}>Phone</label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => updateField('phone', e.target.value)}
              placeholder="+1 (555) 123-4567"
              className={inputClass}
            />
          </div>
          <div>
            <label className={labelClass}>LinkedIn</label>
            <input
              type="url"
              value={formData.linkedin}
              onChange={(e) => updateField('linkedin', e.target.value)}
              placeholder="https://linkedin.com/in/johndoe"
              className={inputClass}
            />
          </div>
        </div>
      </div>

      {/* AI Enhancement Toggle */}
      <div className={`p-4 rounded-lg border ${darkMode ? 'bg-gray-700 border-gray-600' : 'bg-blue-50 border-blue-200'}`}>
        <div className="flex items-center space-x-3">
          <input
            type="checkbox"
            id="ai-enhance"
            checked={formData.enhance_with_ai}
            onChange={(e) => updateField('enhance_with_ai', e.target.checked)}
            className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
          />
          <label htmlFor="ai-enhance" className={`flex items-center space-x-2 text-sm font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
            <FiZap className="text-yellow-500" />
            <span>Enhance descriptions with AI</span>
          </label>
        </div>
        <p className={`text-xs mt-2 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
          Uses AI to improve your work experience and project descriptions for better impact.
        </p>
      </div>

      {/* Education */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
            Education
          </h3>
          <button
            type="button"
            onClick={() => addArrayItem('education', { degree: '', institution: '', year: '', gpa: '' })}
            className={`flex items-center space-x-1 px-3 py-1 rounded-md text-sm font-medium transition-colors ${
              darkMode 
                ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            <FiPlus size={16} />
            <span>Add</span>
          </button>
        </div>
        {formData.education.map((edu, index) => (
          <div key={index} className={`p-4 rounded-lg border mb-4 ${darkMode ? 'border-gray-600' : 'border-gray-200'}`}>
            <div className="flex justify-between items-start mb-3">
              <span className={`text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                Education #{index + 1}
              </span>
              {formData.education.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeArrayItem('education', index)}
                  className="text-red-500 hover:text-red-700 transition-colors"
                >
                  <FiTrash2 size={16} />
                </button>
              )}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <label className={labelClass}>Degree</label>
                <input
                  type="text"
                  value={edu.degree}
                  onChange={(e) => updateArrayField('education', index, 'degree', e.target.value)}
                  placeholder="Bachelor of Science in Computer Science"
                  className={inputClass}
                />
              </div>
              <div>
                <label className={labelClass}>Institution</label>
                <input
                  type="text"
                  value={edu.institution}
                  onChange={(e) => updateArrayField('education', index, 'institution', e.target.value)}
                  placeholder="University of Technology"
                  className={inputClass}
                />
              </div>
              <div>
                <label className={labelClass}>Year</label>
                <input
                  type="text"
                  value={edu.year}
                  onChange={(e) => updateArrayField('education', index, 'year', e.target.value)}
                  placeholder="2020-2024"
                  className={inputClass}
                />
              </div>
              <div>
                <label className={labelClass}>GPA (Optional)</label>
                <input
                  type="text"
                  value={edu.gpa}
                  onChange={(e) => updateArrayField('education', index, 'gpa', e.target.value)}
                  placeholder="3.8/4.0"
                  className={inputClass}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Work Experience */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
            Work Experience
          </h3>
          <button
            type="button"
            onClick={() => addArrayItem('work_experience', { position: '', company: '', duration: '', description: '' })}
            className={`flex items-center space-x-1 px-3 py-1 rounded-md text-sm font-medium transition-colors ${
              darkMode 
                ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            <FiPlus size={16} />
            <span>Add</span>
          </button>
        </div>
        {formData.work_experience.map((exp, index) => (
          <div key={index} className={`p-4 rounded-lg border mb-4 ${darkMode ? 'border-gray-600' : 'border-gray-200'}`}>
            <div className="flex justify-between items-start mb-3">
              <span className={`text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                Experience #{index + 1}
              </span>
              {formData.work_experience.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeArrayItem('work_experience', index)}
                  className="text-red-500 hover:text-red-700 transition-colors"
                >
                  <FiTrash2 size={16} />
                </button>
              )}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
              <div>
                <label className={labelClass}>Position</label>
                <input
                  type="text"
                  value={exp.position}
                  onChange={(e) => updateArrayField('work_experience', index, 'position', e.target.value)}
                  placeholder="Software Engineer"
                  className={inputClass}
                />
              </div>
              <div>
                <label className={labelClass}>Company</label>
                <input
                  type="text"
                  value={exp.company}
                  onChange={(e) => updateArrayField('work_experience', index, 'company', e.target.value)}
                  placeholder="Tech Corp"
                  className={inputClass}
                />
              </div>
              <div className="md:col-span-2">
                <label className={labelClass}>Duration</label>
                <input
                  type="text"
                  value={exp.duration}
                  onChange={(e) => updateArrayField('work_experience', index, 'duration', e.target.value)}
                  placeholder="Jan 2022 - Present"
                  className={inputClass}
                />
              </div>
            </div>
            <div>
              <label className={labelClass}>Description</label>
              <textarea
                value={exp.description}
                onChange={(e) => updateArrayField('work_experience', index, 'description', e.target.value)}
                placeholder="Describe your responsibilities and achievements..."
                rows={3}
                className={inputClass}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Projects */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
            Projects
          </h3>
          <button
            type="button"
            onClick={() => addArrayItem('projects', { title: '', description: '' })}
            className={`flex items-center space-x-1 px-3 py-1 rounded-md text-sm font-medium transition-colors ${
              darkMode 
                ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            <FiPlus size={16} />
            <span>Add</span>
          </button>
        </div>
        {formData.projects.map((project, index) => (
          <div key={index} className={`p-4 rounded-lg border mb-4 ${darkMode ? 'border-gray-600' : 'border-gray-200'}`}>
            <div className="flex justify-between items-start mb-3">
              <span className={`text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                Project #{index + 1}
              </span>
              {formData.projects.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeArrayItem('projects', index)}
                  className="text-red-500 hover:text-red-700 transition-colors"
                >
                  <FiTrash2 size={16} />
                </button>
              )}
            </div>
            <div className="space-y-3">
              <div>
                <label className={labelClass}>Project Title</label>
                <input
                  type="text"
                  value={project.title}
                  onChange={(e) => updateArrayField('projects', index, 'title', e.target.value)}
                  placeholder="E-commerce Website"
                  className={inputClass}
                />
              </div>
              <div>
                <label className={labelClass}>Description</label>
                <textarea
                  value={project.description}
                  onChange={(e) => updateArrayField('projects', index, 'description', e.target.value)}
                  placeholder="Describe the project, technologies used, and your role..."
                  rows={3}
                  className={inputClass}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Skills */}
      <div>
        <h3 className={`text-lg font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
          Skills
        </h3>
        <div>
          <label className={labelClass}>Skills (comma-separated)</label>
          <textarea
            value={formData.skills.join(', ')}
            onChange={(e) => handleSkillsChange(e.target.value)}
            placeholder="JavaScript, React, Node.js, Python, SQL, Git"
            rows={3}
            className={inputClass}
          />
          {formData.skills.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {formData.skills.map((skill, index) => (
                <span
                  key={index}
                  className={`px-3 py-1 rounded-full text-sm ${
                    darkMode 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-blue-100 text-blue-800'
                  }`}
                >
                  {skill}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResumeForm;