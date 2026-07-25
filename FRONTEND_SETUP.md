# Frontend Integration Guide

This guide will help you connect your frontend repository with this Django backend.

## Repository Structure

- **Backend**: `https://github.com/gloriaw12198-lab/Event-Management-backend.git`
- **Frontend**: `https://github.com/gloriaw12198-lab/-Event-Management-frontend.git`

## Backend API Endpoints

### Base URL
- Local: `http://localhost:8000/api`
- Production: `https://your-backend-domain.com/api`

### Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/logout/` - Logout (blacklist refresh token)
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get current user profile

### User Endpoints
- `GET /api/auth/users/` - List all users
- `GET /api/auth/users/{id}/` - Get user details
- `PUT /api/auth/users/{id}/` - Update user
- `DELETE /api/auth/users/{id}/` - Delete user

### Event Endpoints
- `GET /api/events/` - List all events (supports search/filter)
- `POST /api/events/` - Create event (Organizer/Admin)
- `GET /api/events/{id}/` - Get event details
- `PUT /api/events/{id}/` - Update event (Owner/Admin)
- `DELETE /api/events/{id}/` - Delete event (Owner/Admin)

### Category Endpoints
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create category (Organizer/Admin)
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category (Organizer/Admin)
- `DELETE /api/categories/{id}/` - Delete category (Organizer/Admin)

### Venue Endpoints
- `GET /api/venues/` - List all venues
- `POST /api/venues/` - Create venue (Organizer/Admin)
- `GET /api/venues/{id}/` - Get venue details
- `PUT /api/venues/{id}/` - Update venue (Organizer/Admin)
- `DELETE /api/venues/{id}/` - Delete venue (Organizer/Admin)

### Ticket Endpoints
- `GET /api/tickets/` - List all tickets
- `POST /api/tickets/` - Create ticket (Organizer/Admin)
- `GET /api/tickets/{id}/` - Get ticket details
- `PUT /api/tickets/{id}/` - Update ticket (Owner/Admin)
- `DELETE /api/tickets/{id}/` - Delete ticket (Owner/Admin)

### Registration Endpoints
- `GET /api/registrations/` - List registrations (based on role)
- `POST /api/registrations/` - Register for event (Attendee)
- `GET /api/registrations/{id}/` - Get registration details
- `PUT /api/registrations/{id}/` - Update registration
- `DELETE /api/registrations/{id}/` - Cancel registration

## Frontend Setup Instructions

### 1. Clone the Frontend Repository
```bash
git clone https://github.com/gloriaw12198-lab/-Event-Management-frontend.git
cd -Event-Management-frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure API Connection

Create a `.env` file in your frontend root:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 4. Create API Service

Create `src/api.js`:
```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refreshToken,
        });
        
        const { access } = response.data;
        localStorage.setItem('access_token', access);
        
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

### 5. Start the Backend

In a separate terminal:
```bash
cd Event-Management-backend
python manage.py runserver
```

Or with Docker:
```bash
cd Event-Management-backend
docker-compose up
```

### 6. Start the Frontend

```bash
npm run dev
```

## Data Models

### User Model
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "attendee|organizer|admin",
  "phone": "string",
  "profile_image": "string"
}
```

### Event Model
```json
{
  "id": 1,
  "title": "string",
  "description": "string",
  "date": "YYYY-MM-DD",
  "time": "HH:MM:SS",
  "venue": 1,
  "category": 1,
  "organizer": 1,
  "capacity": 100,
  "available_seats": 100,
  "image": "string"
}
```

### Category Model
```json
{
  "id": 1,
  "name": "string",
  "description": "string"
}
```

### Venue Model
```json
{
  "id": 1,
  "name": "string",
  "address": "string",
  "city": "string",
  "capacity": 100,
  "description": "string"
}
```

### Ticket Model
```json
{
  "id": 1,
  "event": 1,
  "ticket_type": "regular|vip|early_bird|student",
  "price": 50.00,
  "quantity": 100,
  "description": "string"
}
```

### Registration Model
```json
{
  "id": 1,
  "attendee": 1,
  "event": 1,
  "ticket": 1,
  "status": "confirmed|pending|cancelled",
  "registration_date": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## Search and Filter Parameters

### Events Search
- `?search=query` - Search by title, description, organizer
- `?category={id}` - Filter by category
- `?venue={id}` - Filter by venue
- `?date_from={date}` - Filter events from date
- `?date_to={date}` - Filter events to date
- `?location={city}` - Filter by venue city
- `?ordering=date` - Order by date, time, title, or capacity

## Authentication Flow

### Login
```javascript
const login = async (username, password) => {
  const response = await api.post('/auth/login/', {
    username,
    password
  });
  
  const { access, refresh } = response.data;
  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
  
  return response.data;
};
```

### Register
```javascript
const register = async (userData) => {
  const response = await api.post('/auth/register/', userData);
  return response.data;
};
```

### Logout
```javascript
const logout = async () => {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    await api.post('/auth/logout/', { refresh_token: refreshToken });
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
};
```

## CORS Configuration

The backend is configured to allow requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

To add your frontend domain, update the backend `.env` file:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://your-frontend-domain.com
```

## Common Issues

### CORS Errors
- Ensure your frontend URL is in `CORS_ALLOWED_ORIGINS`
- Check that the backend is running
- Verify the API base URL in your frontend

### Authentication Errors
- Ensure tokens are stored in localStorage
- Check token expiration (default: 60 minutes)
- Verify token refresh logic

### 401 Unauthorized
- Check that the token is being sent in headers
- Verify the token hasn't expired
- Ensure the user has the required permissions

## Development Workflow

1. Start the backend server
2. Start the frontend development server
3. Make API calls from frontend to backend
4. Test authentication flow
5. Test CRUD operations for each resource
6. Test search and filter functionality

## Production Deployment

### Backend
- Set `DEBUG=False`
- Use a strong `SECRET_KEY`
- Configure production database
- Set up static file serving
- Use HTTPS

### Frontend
- Update `VITE_API_BASE_URL` to production backend URL
- Build the frontend: `npm run build`
- Deploy to your hosting service

## Support

For issues with:
- **Backend**: Check the backend repository issues
- **Frontend**: Check the frontend repository issues
- **Integration**: Ensure both repositories are properly configured