# Event Management Backend

A Django REST Framework backend for an event management system with JWT authentication, role-based access control, and comprehensive event management features.

## Tech Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- Django REST Framework SimpleJWT 5.3.0
- PostgreSQL
- Django ORM
- Docker
- GitHub Actions

## Features

### Authentication
- JWT-based authentication with SimpleJWT
- User registration, login, logout, and token refresh
- Role-based access control (Admin, Organizer, Attendee)

### User Management
- Custom user model with roles
- Profile management with image upload
- Role-based permissions

### Event Management
- Create, read, update, and delete events
- Event categories and venues
- Ticket management with different types
- Event registration system
- Search and filter functionality

### Permissions
- **Admin**: Full access to all resources
- **Organizer**: Create and manage own events, view attendees
- **Attendee**: Register for events, view own registrations

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/logout/` - Logout (blacklist refresh token)
- `POST /api/auth/refresh/` - Refresh access token

### Users
- `GET /api/auth/users/` - List all users
- `GET /api/auth/users/{id}/` - Get user details
- `PUT /api/auth/users/{id}/` - Update user
- `DELETE /api/auth/users/{id}/` - Delete user
- `GET /api/auth/profile/` - Get current user profile
- `PUT /api/auth/profile/` - Update current user profile

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create category (Organizer/Admin)
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category (Organizer/Admin)
- `DELETE /api/categories/{id}/` - Delete category (Organizer/Admin)

### Venues
- `GET /api/venues/` - List all venues
- `POST /api/venues/` - Create venue (Organizer/Admin)
- `GET /api/venues/{id}/` - Get venue details
- `PUT /api/venues/{id}/` - Update venue (Organizer/Admin)
- `DELETE /api/venues/{id}/` - Delete venue (Organizer/Admin)

### Events
- `GET /api/events/` - List all events (with search and filter)
- `POST /api/events/` - Create event (Organizer/Admin)
- `GET /api/events/{id}/` - Get event details
- `PUT /api/events/{id}/` - Update event (Owner/Admin)
- `DELETE /api/events/{id}/` - Delete event (Owner/Admin)

### Tickets
- `GET /api/tickets/` - List all tickets
- `POST /api/tickets/` - Create ticket (Organizer/Admin)
- `GET /api/tickets/{id}/` - Get ticket details
- `PUT /api/tickets/{id}/` - Update ticket (Owner/Admin)
- `DELETE /api/tickets/{id}/` - Delete ticket (Owner/Admin)

### Registrations
- `GET /api/registrations/` - List registrations (based on role)
- `POST /api/registrations/` - Register for event (Attendee)
- `GET /api/registrations/{id}/` - Get registration details
- `PUT /api/registrations/{id}/` - Update registration
- `DELETE /api/registrations/{id}/` - Cancel registration

## Search and Filter

Events can be searched and filtered using query parameters:
- `?search=query` - Search by title, description, or organizer
- `?category={id}` - Filter by category
- `?venue={id}` - Filter by venue
- `?date_from={date}` - Filter events from date
- `?date_to={date}` - Filter events to date
- `?location={city}` - Filter by venue city
- `?ordering=date` - Order by date, time, title, or capacity

## Setup Instructions

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd Event-Management-backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. The application will be available at `http://localhost:8000`

### Running Tests

```bash
python manage.py test
```

## Environment Variables

- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `USE_SQLITE` - Use SQLite instead of PostgreSQL (True/False)
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins

## Project Structure

```
event_management/
├── accounts/          # User authentication and management
├── events/            # Event management
├── categories/        # Event categories
├── venues/            # Venue management
├── tickets/           # Ticket management
├── registrations/     # Event registrations
├── core/              # Core utilities and permissions
├── media/             # User uploaded files
├── static/            # Static files
├── manage.py
└── requirements.txt
```

## CI/CD

The project uses GitHub Actions for continuous integration:
- Runs tests on push and pull requests
- Tests against PostgreSQL database
- Runs migrations and Django checks

## Database Models

### User
- Custom user model extending AbstractUser
- Fields: role, phone, profile_image
- Roles: attendee, organizer, admin

### Event
- Fields: title, description, date, time, venue, category, organizer, capacity, available_seats, image
- Relationships: venue, category, organizer

### Category
- Fields: name, description
- Used for event categorization

### Venue
- Fields: name, address, city, capacity, description
- Physical locations for events

### Ticket
- Fields: event, ticket_type, price, quantity, description
- Ticket types: regular, vip, early_bird, student

### Registration
- Fields: attendee, event, ticket, status, registration_date
- Status: confirmed, pending, cancelled
- Unique constraint on attendee-event pair

## Permissions

### Custom Permissions
- `IsAdmin` - Only admin users
- `IsOrganizer` - Only organizer users
- `IsAttendee` - Only attendee users
- `IsAdminOrOrganizer` - Admin or organizer users
- `IsOwnerOrAdmin` - Resource owner or admin
- `IsOrganizerOrReadOnly` - Organizers can write, others can read
- `IsOrganizerOwnerOrAdmin` - Event organizer or admin can modify

## Development Workflow

1. Create a feature branch from `develop`
2. Implement your changes
3. Run tests locally
4. Commit and push changes
5. Create a pull request to `develop`
6. After review, merge to `develop`
7. Periodically merge `develop` to `main`

## Production Deployment

For production deployment:
1. Set `DEBUG=False`
2. Use a strong `SECRET_KEY`
3. Configure proper database settings
4. Set up static file serving
5. Configure allowed hosts
6. Use HTTPS
7. Set up proper logging
8. Configure CORS for your frontend domain

## License

This project is licensed under the MIT License.