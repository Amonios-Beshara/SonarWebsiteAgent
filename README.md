# HelloSonar AI - Voice Documentation Agent

A real-time voice agent that helps you write documentation collaboratively using LiveKit for audio communication and OpenAI for FAQ generation.

## Features

- 🎤 Real-time voice communication using LiveKit
- 🤖 AI-powered FAQ generation from conversation transcripts
- 📱 Modern React frontend with sky blue/white theme
- 🚀 FastAPI backend with CORS support
- 🔐 Secure token-based authentication

## Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- LiveKit server (self-hosted or cloud)
- OpenAI API key

## Environment Variables

Create a `.env` file in the backend directory:

```env
# LiveKit Configuration
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=wss://your-livekit-server.com

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
```

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (see above)

4. Run the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### POST /create-session
Creates a new LiveKit session for voice communication.

**Request:**
```json
{
  "company": "your_company_name"
}
```

**Response:**
```json
{
  "room_name": "your_company_name_session",
  "token": "livekit_jwt_token",
  "livekit_url": "wss://your-livekit-server.com"
}
```

### POST /generate-faq
Generates FAQ from conversation transcript.

**Request:**
```json
{
  "transcript": "conversation transcript in Arabic"
}
```

**Response:**
```json
{
  "faq": "Generated FAQ content"
}
```

## Deployment

### Backend Deployment (Docker)

1. Create a `Dockerfile` in the backend directory:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. Build and run:
   ```bash
   docker build -t hellosonar-backend .
   docker run -p 8000:8000 --env-file .env hellosonar-backend
   ```

### Frontend Deployment

1. Build the production version:
   ```bash
   npm run build
   ```

2. Deploy the `build` folder to your hosting service (Netlify, Vercel, etc.)

3. Update the API URLs in `src/api.ts` to point to your deployed backend.

### Environment Setup for Production

- Set `LIVEKIT_URL` to your production LiveKit server
- Ensure CORS is properly configured for your domain
- Use environment variables for all sensitive data
- Set up proper SSL certificates

## Development

### Running Tests

Frontend tests:
```bash
cd frontend
npm test
```

Backend tests (if added):
```bash
cd backend
pytest
```

### Code Structure

```
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── api.ts           # API client functions
│   │   └── index.css        # Global styles
│   └── package.json
├── backend/
│   ├── main.py              # FastAPI application
│   ├── agent.py             # LiveKit and OpenAI integration
│   └── requirements.txt
└── README.md
```

## Troubleshooting

### Common Issues

1. **LiveKit Connection Failed**
   - Verify `LIVEKIT_URL` is correct
   - Check if LiveKit server is running
   - Ensure API keys are valid

2. **OpenAI API Errors**
   - Verify `OPENAI_API_KEY` is set
   - Check API key permissions
   - Ensure sufficient credits

3. **CORS Errors**
   - Backend CORS is configured for development
   - Update CORS settings for production domains

4. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 