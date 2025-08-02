// Configuration for API endpoints
const config = {
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  endpoints: {
    health: '/health',
    generate: '/generate',
    preview: '/preview'
  }
};

export default config;