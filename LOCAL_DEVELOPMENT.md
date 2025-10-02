# 🚀 HydroAI - Local Development Setup Guide

This guide will help you set up and run the HydroAI application locally for development purposes.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.11+** (recommended: 3.11 or higher)
- **Node.js 18+** and **npm 8+**
- **Git** for version control

### Optional (for easier development)
- **Docker** and **Docker Compose** (for containerized development)
- **PostgreSQL** (if not using Docker)
- **Redis** (for caching, optional)

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   Next.js       │────│    Flask        │────│  PostgreSQL     │
│   Port: 3000    │    │   Port: 5000    │    │  Port: 5432     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   WebSocket     │
                       │   Port: 8765    │
                       └─────────────────┘
```

## 🛠️ Setup Methods

### Method 1: Docker Compose (Recommended for beginners)

#### 1. Clone the Repository
```bash
git clone https://github.com/kumarraviraj549/ai-hydroponic-farming.git
cd ai-hydroponic-farming
```

#### 2. Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

#### 3. Initialize Database
```bash
# Initialize database with demo data
docker-compose exec backend python init_db.py
```

#### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **pgAdmin** (optional): http://localhost:8080

### Method 2: Manual Setup (For development)

#### 1. Clone and Setup Repository
```bash
git clone https://github.com/kumarraviraj549/ai-hydroponic-farming.git
cd ai-hydroponic-farming
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv hydroai_env

# Activate virtual environment
# On Windows:
hydroai_env\Scripts\activate
# On macOS/Linux:
source hydroai_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your configurations
# For SQLite (simpler setup):
echo "DATABASE_URL=sqlite:///hydroai.db" >> .env
echo "SECRET_KEY=your-secret-key-here" >> .env
echo "JWT_SECRET_KEY=your-jwt-secret-here" >> .env

# Initialize database
python init_db.py

# Start the Flask server
python app.py
```

#### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Start the Next.js development server
npm run dev
```

#### 4. WebSocket Server (Optional)

```bash
# In another terminal, navigate to backend
cd backend
source hydroai_env/bin/activate  # On Windows: hydroai_env\Scripts\activate

# Start WebSocket server
python websocket_server.py
```

## 🔧 Configuration Files

### Backend Environment Variables (.env)

```bash
# Database
DATABASE_URL=sqlite:///hydroai.db
# For PostgreSQL: DATABASE_URL=postgresql://user:pass@localhost:5432/hydroai

# Security
SECRET_KEY=generate-a-secure-random-key-here
JWT_SECRET_KEY=generate-jwt-secret-here

# Development settings
FLASK_ENV=development
DEMO_MODE=true
DEBUG=true

# Optional: External services
# MAIL_SERVER=smtp.gmail.com
# MAIL_USERNAME=your-email@gmail.com
# WEATHER_API_KEY=your-weather-api-key
```

### Frontend Environment Variables (.env.local)

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8765

# App Configuration
NEXT_PUBLIC_DEMO_MODE=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

## 🗄️ Database Setup

### SQLite (Recommended for development)
- No additional setup required
- Database file: `backend/hydroai.db`
- Automatic creation on first run

### PostgreSQL (Production-like setup)

#### Option A: Using Docker
```bash
# Start only PostgreSQL
docker-compose up postgres -d
```

#### Option B: Local PostgreSQL Installation
```bash
# Install PostgreSQL (varies by OS)
# Ubuntu/Debian:
sudo apt install postgresql postgresql-contrib

# macOS with Homebrew:
brew install postgresql

# Create database
sudo -u postgres createdb hydroai
sudo -u postgres createuser hydroai

# Update .env file
DATABASE_URL=postgresql://hydroai:password@localhost:5432/hydroai
```

## 🎯 Available Scripts

### Root Directory Scripts
```bash
# Install all dependencies
npm run install:all

# Start both frontend and backend
npm run dev

# Build frontend
npm run build

# Initialize database
npm run init:db

# Seed demo data
npm run seed:db
```

### Backend Scripts
```bash
# Start Flask server
python app.py

# Initialize database
python init_db.py

# Seed demo data
python seed_demo_data.py

# Start WebSocket server
python websocket_server.py

# Run tests
python -m pytest
```

### Frontend Scripts
```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

## 🧪 Demo Data

The application includes comprehensive demo data:

### Demo User Credentials
- **Email**: demo@hydroai.com
- **Password**: demo123

### Included Demo Data
- **3 Demo Farms**: Greenhouse, Vertical, Hydroponic units
- **12 Sensors**: Temperature, humidity, pH, nutrient sensors
- **7 Days of Historical Data**: Realistic sensor readings
- **AI Recommendations**: Sample optimization suggestions
- **Alert System**: Example notifications

## 🔍 API Testing

### Health Check
```bash
curl http://localhost:5000/api/v1/health
```

### Authentication
```bash
# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@hydroai.com","password":"demo123"}'
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :3000  # for frontend
lsof -i :5000  # for backend

# Kill the process
kill -9 <PID>
```

#### Database Connection Issues
```bash
# Check database connection
cd backend
python init_db.py --check-connection

# Reset database
python init_db.py --drop
```

#### Module Import Errors
```bash
# Ensure virtual environment is activated
source hydroai_env/bin/activate  # Linux/macOS
# or
hydroai_env\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Frontend Build Issues
```bash
# Clear Next.js cache
npm run clean

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Log Files
- Backend logs: `backend/logs/hydroai.log`
- Frontend logs: Browser console and terminal
- Database logs: Docker logs for postgres service

## 📊 Development Tools

### Recommended VS Code Extensions
- Python
- Pylance
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Docker
- GitLens

### Database Management
- **pgAdmin**: http://localhost:8080 (when using Docker)
- **DBeaver**: Universal database tool
- **SQLite Browser**: For SQLite databases

## 🚀 Next Steps

1. **Explore the API**: Use the Swagger documentation at `/api/v1/docs`
2. **Customize**: Modify the demo data in `backend/seed_demo_data.py`
3. **Extend**: Add new features following the existing patterns
4. **Deploy**: Check `DEPLOYMENT.md` for production deployment guides

## 📞 Getting Help

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Documentation**: Check the README.md and other documentation files

---

**Happy Coding! 🌱**