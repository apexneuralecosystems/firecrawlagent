# FireCrawl Agent API Documentation

This document lists the available API endpoints for the FireCrawl Agent project.

## Base URL
Default: `http://localhost:8000`

## Endpoints

### Health Check
- **GET** `/`
    - **Description**: Basic API health check.
    - **Response**: `{"message": "FireCrawl Agent API", "status": "running", "version": "1.0.0"}`

- **GET** `/api/health`
    - **Description**: Detailed health check including environment status.
    - **Response**: `{"status": "healthy", "sessions": int, "environment": {...}}`

### Document Management
- **POST** `/api/upload`
    - **Description**: Upload and process a PDF document.
    - **Request**: Multipart Form Data (`file`: PDF file)
    - **Response**: `{"session_id": "uuid", "filename": "name.pdf", "status": "processed", "uploaded_at": "timestamp"}`

### Chat / Workflow
- **POST** `/api/chat`
    - **Description**: Send a message to the RAG agent for a specific session.
    - **Request**:
        ```json
        {
          "session_id": "uuid",
          "message": "your question here"
        }
        ```
    - **Response**:
        ```json
        {
          "response": "agent answer",
          "session_id": "uuid",
          "logs": "optional logs"
        }
        ```

### Session Management
- **GET** `/api/sessions`
    - **Description**: List all active sessions.
    - **Response**: `{"sessions": [...], "count": int}`

- **GET** `/api/sessions/{session_id}`
    - **Description**: Get details for a specific session.
    - **Response**: Session object (excluding workflow object).

- **DELETE** `/api/sessions/{session_id}`
    - **Description**: Delete a session and cleanup resources.
    - **Response**: `{"status": "deleted", "session_id": "uuid"}`

## Authentication (Backend Only)
> **Note**: These endpoints exist in the backend but are currently **not used** by the frontend interface.

- **POST** `/api/auth/signup`
    - **Request**: `{"email": "...", "password": "...", "first_name": "...", "last_name": "...", "username": "..."}`
    - **Response**: `{"id": "...", "email": "..."}`

- **POST** `/api/auth/login`
    - **Request**: `{"email": "...", "password": "..."}`
    - **Response**: `Token` object (JWT).

- **POST** `/api/auth/refresh`
    - **Request**: `{"refresh_token": "..."}`
    - **Response**: `Token` object.

- **POST** `/api/auth/forgot-password`
    - **Request**: `{"email": "..."}`
    - **Response**: `{"ok": True, "reset_token": "..."}`

- **POST** `/api/auth/reset-password`
    - **Request**: `{"token": "...", "new_password": "..."}`
    - **Response**: `{"ok": bool}`

- **POST** `/api/auth/change-password`
    - **Request**: `{"user_id": "...", "old_password": "...", "new_password": "..."}`
    - **Response**: `{"ok": bool}`
