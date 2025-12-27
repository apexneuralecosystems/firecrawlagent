# FastAPI Application with Apex SaaS Framework

## Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file (optional):
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-minimum-32-characters-long
```

### 4. Run the Application
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Features

- **Automatic Table Creation**: Tables are created automatically on startup from your models
- **Authentication**: User signup, login, logout, password reset
- **Payments**: PayPal order creation and capture
- **API Documentation**: Available at `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `POST /api/forgot-password` - Request password reset
- `POST /api/reset-password` - Reset password with token

### Payments
- `POST /api/payments/create-order` - Create PayPal order
- `POST /api/payments/capture-order` - Capture PayPal order
- `GET /api/payments/order/{order_id}` - Get order details

## Project Structure

- `main.py` - FastAPI application and endpoints
- `app.py` - Business logic functions
- `models.py` - Database models (User, Payment)
- `requirements.txt` - Python dependencies

## Notes

- Tables are automatically created on startup via `bootstrap()`
- Uses async PostgreSQL with asyncpg driver
- All models must use `@register_model` decorator

