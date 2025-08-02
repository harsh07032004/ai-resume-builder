import React from 'react';

const ResumePreview = ({ html, darkMode }) => {
  return (
    <div className="h-96 overflow-auto">
      <div 
        className={`prose max-w-none ${darkMode ? 'prose-invert' : ''}`}
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </div>
  );
};

export default ResumePreview;