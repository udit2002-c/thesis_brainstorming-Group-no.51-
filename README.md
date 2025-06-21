# Thesis Brainstorming Tool

A production-ready, AI-powered thesis idea generator that helps students and researchers brainstorm innovative thesis topics with enterprise-grade security and performance.

## 🚀 Features

- **AI-Powered Generation**: Uses Groq API with Llama models for high-quality thesis ideas
- **Multiple Thesis Types**: Argumentative, analytical, expository, comparative
- **Tone Selection**: Academic, persuasive, neutral, critical
- **Security First**: Rate limiting, CORS protection, input validation, security headers
- **Production Ready**: Health checks, monitoring, error handling, logging
- **Intelligent Fallback**: Enhanced mock system when APIs are unavailable
- **Modern UI**: Academic-themed interface with responsive design
- **Performance Optimized**: Caching, compression, efficient static file serving

## 🏗️ Architecture

```
├── main.py              # Production FastAPI application
├── config.py            # Centralized configuration
├── prompt_templates.py  # AI prompt templates and mock data
├── deploy.py           # Production deployment validator
├── templates/          # Jinja2 HTML templates
├── static/            # CSS, images, and assets
├── requirements.txt   # Python dependencies
└── vercel.json       # Vercel deployment configuration
```

## 🔧 Production Setup

### Prerequisites
- Python 3.11+
- Git
- Vercel CLI (for deployment)

### Local Development

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd thesis_brainstorming-Group-no.51-
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   # Required for API functionality
   export GROQ_API_KEY=your_groq_api_key_here
   
   # Optional production settings
   export MAX_REQUESTS_PER_MINUTE=10
   export REQUEST_TIMEOUT=30
   export ALLOWED_ORIGINS=https://yourdomain.com
   ```

3. **Run Development Server**
   ```bash
   python3 main.py
   ```
   Access at: http://localhost:8001

### Production Deployment

#### Vercel Deployment (Recommended)

1. **Pre-deployment Validation**
   ```bash
   python3 deploy.py
   ```

2. **Deploy to Vercel**
   ```bash
   # Install Vercel CLI
   npm i -g vercel
   
   # Deploy
   vercel --prod
   ```

3. **Set Environment Variables in Vercel Dashboard**
   - `GROQ_API_KEY`: Your Groq API key
   - `ALLOWED_ORIGINS`: Your domain (optional)
   - `MAX_REQUESTS_PER_MINUTE`: Rate limit (optional)

#### Manual Server Deployment

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   export GROQ_API_KEY=your_key
   export VERCEL=1  # Enables production mode
   ```

3. **Run with Production Server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4
   ```

## 🔐 Security Features

- **Rate Limiting**: Configurable per-IP rate limiting
- **CORS Protection**: Configurable allowed origins
- **Security Headers**: XSS, CSRF, content-type protection
- **Input Validation**: Comprehensive request validation
- **Directory Traversal Protection**: Secure static file serving
- **Error Handling**: No sensitive information leakage

## 📊 Monitoring & Health Checks

### Health Endpoints

- **`/health`**: Basic health check
- **`/health/ready`**: Readiness probe for deployments
- **`/check-api-status`**: API connectivity status

### Monitoring Features

- **Structured Logging**: JSON logs with timestamps and levels
- **Performance Metrics**: Request timing headers
- **Error Tracking**: Comprehensive error logging
- **API Status Monitoring**: Real-time API health checks

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | - | Groq API key (get from console.groq.com) |
| `MAX_REQUESTS_PER_MINUTE` | 10 | Rate limit per IP |
| `REQUEST_TIMEOUT` | 30 | API request timeout (seconds) |
| `ALLOWED_ORIGINS` | * | CORS allowed origins (comma-separated) |
| `PORT` | 8001 | Server port |
| `VERCEL` | - | Production mode flag (auto-set by Vercel) |

### API Configuration

The application supports multiple AI providers:

1. **Groq API** (Primary)
   - Fast inference with Llama models
   - Get free API key: https://console.groq.com/keys
   - Rate limits: Generous free tier

2. **Enhanced Mock System** (Fallback)
   - Intelligent thesis generation
   - No API key required
   - Production-ready fallback

## 🚀 Performance Optimizations

- **Static File Caching**: 24-hour cache headers
- **Compression**: Gzip compression for text assets
- **Async Processing**: Non-blocking API calls
- **Connection Pooling**: Efficient HTTP client usage
- **Minimal Dependencies**: Lightweight production build

## 🔍 Troubleshooting

### Common Issues

1. **Rate Limit Exceeded**
   ```
   Solution: Increase MAX_REQUESTS_PER_MINUTE or implement user authentication
   ```

2. **API Timeout**
   ```
   Solution: Increase REQUEST_TIMEOUT or check network connectivity
   ```

3. **CORS Errors**
   ```
   Solution: Add your domain to ALLOWED_ORIGINS environment variable.
   ```

4. **Static Files Not Loading**
   ```
   Solution: Check file permissions and paths, verify /debug/static endpoint
   ```

### Debug Endpoints

- **`/debug/static`**: View static file configuration
- **`/models`**: Check available AI models
- **`/check-api-status`**: Test API connectivity

## 📈 Scaling Considerations

### Horizontal Scaling
- Stateless design enables multiple instances
- Rate limiting uses in-memory storage (consider Redis for multi-instance)
- Health checks support load balancer integration

### Performance Tuning
- Adjust `MAX_REQUESTS_PER_MINUTE` based on usage patterns
- Monitor `REQUEST_TIMEOUT` for optimal user experience
- Use CDN for static assets in high-traffic scenarios

### Database Integration
- Currently stateless (no database required)
- Easy to add PostgreSQL/MongoDB for user management
- Session storage can be added for authenticated users

## 🛠️ Development

### Code Structure
- **FastAPI**: Modern async web framework
- **Pydantic**: Data validation and settings management
- **HTTPX**: Async HTTP client for API calls
- **Jinja2**: Template engine for server-side rendering

### Testing
```bash
# Run deployment validation
python3 deploy.py

# Test API endpoints
curl http://localhost:8001/health
curl http://localhost:8001/check-api-status
```

### Contributing
1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Update tests for new features
4. Run deployment validation before commits

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For production support:
1. Check health endpoints for system status
2. Review application logs for error details
3. Validate environment configuration
4. Test API connectivity

**Production Checklist**: Run `python3 deploy.py` before any deployment to ensure all systems are ready. 