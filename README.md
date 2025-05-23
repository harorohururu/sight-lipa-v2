# Tourist Monitoring System - Lipa City

A Flask-based web application to log and monitor tourist visits across landmarks in Lipa City using QR codes.

## Project Structure

- `app/` - Main application package
- `migrations/` - Database migration scripts
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `run.py` - App entry point

## Setup Instructions

1. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the application:
   ```powershell
   python run.py
   ```

## Features
- Admin interface for managing landmarks
- QR code generation for each landmark
- Tourist visit logging via QR code scan
- Real-time and historical visit monitoring
