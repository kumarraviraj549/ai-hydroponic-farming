#!/usr/bin/env python3
"""Setup script for HydroAI local development environment."""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, cwd=cwd, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_requirements():
    """Check if required software is installed."""
    print("Checking requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✓ Python {python_version.major}.{python_version.minor}")
    
    # Check Node.js
    success, output = run_command("node --version")
    if not success:
        print("❌ Node.js is required but not found")
        return False
    print(f"✓ Node.js {output.strip()}")
    
    # Check npm
    success, output = run_command("npm --version")
    if not success:
        print("❌ npm is required but not found")
        return False
    print(f"✓ npm {output.strip()}")
    
    return True

def setup_backend():
    """Setup backend environment."""
    print("\n🔧 Setting up backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    os.chdir(backend_dir)
    
    # Create virtual environment
    print("Creating virtual environment...")
    success, _ = run_command(f"{sys.executable} -m venv venv")
    if not success:
        print("❌ Failed to create virtual environment")
        return False
    
    # Determine virtual environment activation command
    if os.name == 'nt':  # Windows
        venv_python = "venv\\Scripts\\python"
        venv_pip = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        venv_python = "venv/bin/python"
        venv_pip = "venv/bin/pip"
    
    # Upgrade pip
    print("Upgrading pip...")
    success, _ = run_command(f"{venv_python} -m pip install --upgrade pip")
    if not success:
        print("⚠️ Failed to upgrade pip, continuing...")
    
    # Install requirements
    print("Installing Python dependencies...")
    success, _ = run_command(f"{venv_pip} install -r requirements.txt")
    if not success:
        print("❌ Failed to install Python dependencies")
        return False
    
    # Setup environment file
    if not os.path.exists(".env"):
        print("Creating .env file...")
        shutil.copy(".env.example", ".env")
        print("✓ Created .env file from template")
    else:
        print("✓ .env file already exists")
    
    os.chdir("..")
    print("✓ Backend setup completed")
    return True

def setup_frontend():
    """Setup frontend environment."""
    print("\n🎨 Setting up frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    os.chdir(frontend_dir)
    
    # Install npm dependencies
    print("Installing Node.js dependencies...")
    success, _ = run_command("npm install")
    if not success:
        print("❌ Failed to install Node.js dependencies")
        return False
    
    # Setup environment file
    if not os.path.exists(".env.local"):
        print("Creating .env.local file...")
        shutil.copy(".env.local.example", ".env.local")
        print("✓ Created .env.local file from template")
    else:
        print("✓ .env.local file already exists")
    
    os.chdir("..")
    print("✓ Frontend setup completed")
    return True

def seed_database():
    """Seed the database with demo data."""
    print("\n🌱 Seeding database with demo data...")
    
    backend_dir = Path("backend")
    os.chdir(backend_dir)
    
    # Determine python executable in virtual environment
    if os.name == 'nt':  # Windows
        venv_python = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        venv_python = "venv/bin/python"
    
    # Run seed script
    success, output = run_command(f"{venv_python} seed_demo_data.py")
    if not success:
        print(f"❌ Failed to seed database: {output}")
        return False
    
    print(output)
    os.chdir("..")
    return True

def print_instructions():
    """Print final setup instructions."""
    print("\n" + "="*60)
    print("🎉 HydroAI Setup Complete!")
    print("="*60)
    print()
    print("To start the development servers:")
    print()
    print("Backend (Terminal 1):")
    if os.name == 'nt':  # Windows
        print("  cd backend")
        print("  venv\\Scripts\\activate")
        print("  python app.py")
    else:  # Unix/Linux/macOS
        print("  cd backend")
        print("  source venv/bin/activate")
        print("  python app.py")
    print()
    print("Frontend (Terminal 2):")
    print("  cd frontend")
    print("  npm run dev")
    print()
    print("WebSocket Server (Terminal 3 - Optional):")
    if os.name == 'nt':  # Windows
        print("  cd backend")
        print("  venv\\Scripts\\activate")
        print("  python websocket_server.py")
    else:  # Unix/Linux/macOS
        print("  cd backend")
        print("  source venv/bin/activate")
        print("  python websocket_server.py")
    print()
    print("Access Points:")
    print("  - Frontend: http://localhost:3000")
    print("  - Backend API: http://localhost:5000/api/v1")
    print("  - API Health: http://localhost:5000/api/v1/health")
    print()
    print("Demo Credentials:")
    print("  Email: demo@hydroai.com")
    print("  Password: demo123")
    print()
    print("="*60)

def main():
    """Main setup function."""
    print("🚀 HydroAI Development Environment Setup")
    print("="*50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        sys.exit(1)
    
    # Seed database
    seed_success = seed_database()
    if not seed_success:
        print("⚠️ Database seeding failed, but setup can continue")
        print("You can run the seed script manually later.")
    
    # Print instructions
    print_instructions()

if __name__ == "__main__":
    main()