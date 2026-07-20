# Flask Student Management System

A comprehensive REST API for managing student information built with Flask and SQLite.

## Features

- CRUD operations for student records
- RESTful API design
- SQLAlchemy ORM for database operations
- Request validation using Marshmallow
- Error handling
- SQLite database integration
- Pagination support
- Sample data generation

## Project Structure

```
student-management-api/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── student.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── students.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── student_schema.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── decorators.py
├── config.py
├── run.py
├── seed_data.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.py` to set your database and Flask configuration.

## Running the Application

1. Generate sample data:
   ```bash
   python seed_data.py
   ```

2. Run the application:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Get All Students
**GET** `/api/students`

Query Parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)

Response:
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 12,
    "pages": 2
  }
}
```

### Get Student by ID
**GET** `/api/students/<id>`

Response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice Johnson",
    "department": "Computer Science",
    "cgpa": 3.9,
    "email": "alice.johnson@student.edu",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

### Create Student
**POST** `/api/students`

Request Body:
```json
{
  "name": "John Doe",
  "department": "Computer Science",
  "cgpa": 3.8,
  "email": "john@example.com"
}
```

Response (201 Created):
```json
{
  "success": true,
  "data": {
    "id": 13,
    "name": "John Doe",
    "department": "Computer Science",
    "cgpa": 3.8,
    "email": "john@example.com",
    "created_at": "2024-01-15T10:35:00",
    "updated_at": "2024-01-15T10:35:00"
  }
}
```

### Update Student
**PUT** `/api/students/<id>`

Request Body (partial update):
```json
{
  "cgpa": 3.95,
  "department": "Data Science"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice Johnson",
    "department": "Data Science",
    "cgpa": 3.95,
    "email": "alice.johnson@student.edu",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:40:00"
  }
}
```

### Delete Student
**DELETE** `/api/students/<id>`

Response (204 No Content):
```json
{
  "success": true,
  "message": "Student deleted successfully"
}
```

## Database

The application uses SQLite for data persistence. The database file `student_management.db` is created automatically in the project root directory.

### Student Model Fields
- `id` (Integer): Primary key
- `name` (String): Student's full name
- `department` (String): Department name
- `cgpa` (Float): Cumulative Grade Point Average (0.0 - 4.0)
- `email` (String): Unique email address
- `created_at` (DateTime): Record creation timestamp
- `updated_at` (DateTime): Last update timestamp

## Technologies Used

- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- SQLAlchemy 2.0.21
- Marshmallow 3.x (for schema validation)
- SQLite3
- Python 3.8+

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK`: Successful GET/PUT request
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate email or other constraint violation
- `500 Internal Server Error`: Server error

## Validation

All inputs are validated:
- **Name**: Required, max 100 characters
- **Department**: Required, max 100 characters
- **CGPA**: Required, must be between 0.0 and 4.0
- **Email**: Required, must be valid email format and unique

## Future Enhancements

- Authentication and authorization
- Advanced filtering and search
- Bulk operations
- Export to CSV/Excel
- Email notifications
- Student performance analytics
- Attendance tracking
- Grade management
