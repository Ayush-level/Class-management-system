# Class Management System - SQLAlchemy Core Implementation

This project implements a class management system database using SQLAlchemy Core based on the Proxima Project schema.

# Service Layer Architecture

This directory contains the service layer implementation that separates business logic from the Flask API and database operations.

## Architecture Overview

```
Flask API Layer → Service Layer → Database Layer (SQLAlchemy Core)
```

## Directory Structure

```
backend/
├── services/              # Service layer
│   ├── __init__.py       # Service initialization
│   ├── base_service.py   # Base service with common functionality
│   ├── class_service.py  # Class management operations
│   ├── student_service.py # Student management operations
│   ├── enrollment_service.py # Enrollment operations
│   └── attendance_service.py # Attendance operations
├── dto/                   # Data Transfer Objects
│   └── __init__.py       # DTOs for data validation and transformation
├── exceptions/            # Custom exceptions
│   └── __init__.py       # Service layer exceptions
├── examples/              # Usage examples
│   └── service_usage_examples.py
├── Dashboard_updated.py   # Updated Flask routes using services
├── attendence_updated.py  # Updated attendance routes
├── classes.py            # Updated class routes
└── requirements.txt      # Dependencies
```

## Key Components

### 1. Services (`services/`)

**BaseService**: Provides common database operations and error handling
- Database connection management
- CRUD operations (create, read, update, delete)
- Query execution with error handling
- Transaction management

**Specific Services**:
- **ClassService**: Class CRUD operations, student listing
- **StudentService**: Student CRUD operations, validation
- **EnrollmentService**: Enrollment management, statistics
- **AttendanceService**: Attendance tracking, bulk operations

### 2. DTOs (`dto/`)

Data Transfer Objects for:
- Data validation
- Type safety
- API response formatting
- Business logic separation

### 3. Exceptions (`exceptions/`)

Custom exceptions for:
- **ServiceException**: Base service exception
- **ValidationException**: Data validation errors
- **NotFoundException**: Resource not found
- **DuplicateResourceException**: Duplicate resource errors
- **BusinessRuleException**: Business rule violations

## Database Schema

The database consists of 5 main tables:

### 1. Classes Table
- `class_id` (String, Primary Key, Unique)
- `class` (Integer, 1 to 5)
- `section` (String)

### 2. General Profile Table
- `student_id` (String, Foreign Key to Enrollment Profile)
- `name` (String)
- `father_name` (String)
- `mother_name` (String)
- `date_of_birth` (Date)
- `gender` (String, 'M' or 'F' or 'T')
- `phone_number` (String, 10 digits)
- `email` (String)
- `blood_group` (String)
- `address` (String)

### 3. Enrollment Profile Table
- `student_id` (String, Primary Key)
- `class_id` (String, Foreign Key to Classes)
- `roll_no` (Integer)
- `date_of_admission` (Date)
- `admission_no` (Integer)
- `status_of_previous_academic_year` (String, 'None' or 'Self' or 'Other')

### 4. Test Metadata Table
- `test_id` (String, Primary Key)
- `test_name` (String)
- `test_date` (Date)
- `subject_1` to `subject_6` (String)
- `subject_1_max_marks` to `subject_6_max_marks` (Integer)

### 5. Test Table
- `student_id` (String, Foreign Key to Enrollment Profile)
- `test_id` (String, Foreign Key to Test Metadata)
- `subject` (Integer, 1 to 6)
- `marks_obtained` (Integer, -1 if not appeared, 0 to max marks)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Setup

```python
from database import get_database_manager, initialize_database

# Initialize database with default SQLite file
db_manager = initialize_database()

# Or with custom database URL
db_manager = initialize_database("postgresql://user:password@localhost/class_management")
```

### Database Operations

```python
from sqlalchemy import insert, select, update, delete
from database import get_database_manager

# Get database manager
db_manager = get_database_manager()
engine = db_manager.get_engine()

# Insert data
with engine.connect() as conn:
    # Insert a new class
    conn.execute(
        insert(db_manager.get_table('classes')).values(
            class_id="CLASS_2_B",
            class=2,
            section="B"
        )
    )
    conn.commit()

# Query data
with engine.connect() as conn:
    # Get all classes
    result = conn.execute(select(db_manager.get_table('classes')))
    for row in result:
        print(f"Class ID: {row.class_id}, Class: {row.class}, Section: {row.section}")
```

### Running the Example

```bash
python example_usage.py
```

This will:
1. Create a SQLite database with all tables
2. Insert sample data
3. Demonstrate various queries

## File Structure

- `database.py` - Core SQLAlchemy implementation with table definitions and DatabaseManager class
- `example_usage.py` - Example usage demonstrating CRUD operations
- `requirements.txt` - Python dependencies
- `README.md` - This documentation

## Database Relationships

- `general_profile.student_id` → `enrollment_profile.student_id` (One-to-One)
- `enrollment_profile.class_id` → `classes.class_id` (Many-to-One)
- `test.student_id` → `enrollment_profile.student_id` (Many-to-One)
- `test.test_id` → `test_metadata.test_id` (Many-to-One)

## Features

- **SQLAlchemy Core**: Uses SQLAlchemy Core for maximum performance and control
- **Type Safety**: Proper column types and constraints
- **Foreign Keys**: Enforced relationships between tables
- **Database Agnostic**: Works with SQLite, PostgreSQL, MySQL, etc.
- **Transaction Support**: Proper transaction handling
- **Example Usage**: Complete examples showing common operations
