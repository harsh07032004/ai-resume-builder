# Deployment Guide - AI Resume Generator

This guide covers how to deploy the AI Resume Generator in various environments.

## Quick Start (Development)

1. **Clone and start everything:**
```bash
git clone <repository-url>
cd ai-resume-generator
./start.sh
```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Manual Setup

### Prerequisites

- **System Requirements:**
  - Ubuntu/Debian Linux (recommended)
  - Python 3.8+ with pip
  - Node.js 16+ with npm
  - LaTeX distribution (texlive)

- **Install system dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nodejs npm
sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended

# Verify installations
python3 --version
node --version
pdflatex --version
```

### Backend Setup

1. **Create and activate virtual environment:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start the Flask server:**
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Install Node.js dependencies:**
```bash
cd frontend
npm install
```

2. **Start the React development server:**
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Production Deployment

### Using Docker (Recommended)

Create `Dockerfile` for backend:
```dockerfile
FROM python:3.9-slim

# Install LaTeX
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
EXPOSE 5000

CMD ["python", "app.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
  
  frontend:
    image: node:16-alpine
    working_dir: /app
    volumes:
      - ./frontend:/app
    ports:
      - "3000:3000"
    command: sh -c "npm install && npm start"
    depends_on:
      - backend
```

### Using systemd (Linux)

1. **Create backend service:**
```ini
# /etc/systemd/system/resume-backend.service
[Unit]
Description=AI Resume Generator Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ai-resume-generator/backend
Environment=PATH=/opt/ai-resume-generator/backend/venv/bin
ExecStart=/opt/ai-resume-generator/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. **Enable and start service:**
```bash
sudo systemctl enable resume-backend
sudo systemctl start resume-backend
```

### Using Nginx (Reverse Proxy)

```nginx
# /etc/nginx/sites-available/resume-generator
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # API Backend
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Environment Variables

### Backend (.env file)
```bash
FLASK_ENV=production
FLASK_DEBUG=False
AI_MODEL_CACHE_DIR=/tmp/transformers_cache
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### Frontend (.env file)
```bash
REACT_APP_API_URL=http://localhost:5000
GENERATE_SOURCEMAP=false
```

## Performance Optimization

### Backend Optimizations

1. **Use Gunicorn for production:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Configure AI model caching:**
```python
# In app.py
import os
os.environ['TRANSFORMERS_CACHE'] = '/tmp/transformers_cache'
```

### Frontend Optimizations

1. **Build for production:**
```bash
npm run build
```

2. **Serve static files with Nginx:**
```nginx
location / {
    root /opt/ai-resume-generator/frontend/build;
    try_files $uri $uri/ /index.html;
}
```

## Monitoring and Logging

### Backend Logging
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('/var/log/resume-generator.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks
- Backend: `GET http://localhost:5000/health`
- Frontend: Check if React app loads

## Security Considerations

1. **CORS Configuration:**
   - Configure allowed origins in production
   - Use environment variables for API URLs

2. **Rate Limiting:**
   - Implement rate limiting for API endpoints
   - Use Redis for distributed rate limiting

3. **File Upload Security:**
   - Validate file types and sizes
   - Scan uploaded content

4. **HTTPS:**
   - Use SSL certificates in production
   - Redirect HTTP to HTTPS

## Troubleshooting

### Common Issues

1. **LaTeX compilation fails:**
   - Ensure all LaTeX packages are installed
   - Check file permissions in temp directories

2. **AI model loading errors:**
   - Verify internet connection for first run
   - Check available memory (>2GB recommended)

3. **CORS errors:**
   - Update CORS origins in Flask app
   - Check API URL configuration

4. **Port conflicts:**
   - Change ports in configuration files
   - Check for other services using ports 3000/5000

### Logs and Debugging

- Backend logs: Check Flask console output
- Frontend logs: Check browser developer console
- System logs: `journalctl -u resume-backend`

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple backend instances
- Use Redis for session storage

### Vertical Scaling
- Increase server resources
- Optimize AI model loading
- Use GPU acceleration for AI models

## Backup and Recovery

1. **Application Code:**
   - Use Git for version control
   - Regular repository backups

2. **Generated Files:**
   - Backup generated PDF directory
   - Consider cloud storage integration

3. **Configuration:**
   - Backup environment files
   - Document custom configurations