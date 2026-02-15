from sqlalchemy import (
    create_engine, MetaData, Table, Column, 
    String, Integer, Date, ForeignKey
)
from sqlalchemy.engine import Engine
from typing import Optional
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()

user = os.environ["DB_USER"]
password = quote_plus(os.environ["DB_PASSWORD"])   # VERY IMPORTANT
host = os.environ["DB_HOST"]
port = os.environ["DB_PORT"]
database = os.environ["DB_NAME"]

DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

metadata = MetaData()

# Classes Table
classes = Table(
    'classes',
    metadata,
    Column('class_id', String, primary_key=True, unique=True),
    Column('class', Integer, nullable=False),  # 1 to 5
    Column('section', String, nullable=False)
)

# General Profile Table
general_profile = Table(
    'general_profile',
    metadata,
    Column('student_id', String, ForeignKey('enrollment_profile.student_id'), primary_key=True),
    Column('name', String, nullable=False),
    Column('father_name', String, nullable=False),
    Column('mother_name', String, nullable=False),
    Column('date_of_birth', Date, nullable=False),
    Column('gender', String, nullable=False),  # 'M' or 'F' or 'T'
    Column('phone_number', String(10), nullable=False),
    Column('email', String, nullable=False),
    Column('blood_group', String, nullable=False),
    Column('address', String, nullable=False)
)

# Enrollment Profile Table
enrollment_profile = Table(
    'enrollment_profile',
    metadata,
    Column('student_id', String, primary_key=True),
    Column('class_id', String, ForeignKey('classes.class_id'), nullable=False),
    Column('roll_no', Integer, nullable=False),
    Column('date_of_admission', Date, nullable=False),
    Column('admission_no', Integer, nullable=False),
    Column('status_of_previous_academic_year', String, nullable=False)  # 'None' or 'Self' or 'Other'
)

# Test Metadata Table
test_metadata = Table(
    'test_metadata',
    metadata,
    Column('test_id', String, primary_key=True),
    Column('test_name', String, nullable=False),
    Column('test_date', Date, nullable=False),
    Column('subject_1', String, nullable=False),
    Column('subject_1_max_marks', Integer, nullable=False),
    Column('subject_2', String, nullable=False),
    Column('subject_2_max_marks', Integer, nullable=False),
    Column('subject_3', String, nullable=False),
    Column('subject_3_max_marks', Integer, nullable=False),
    Column('subject_4', String, nullable=False),
    Column('subject_4_max_marks', Integer, nullable=False),
    Column('subject_5', String, nullable=False),
    Column('subject_5_max_marks', Integer, nullable=False),
    Column('subject_6', String, nullable=False),
    Column('subject_6_max_marks', Integer, nullable=False)
)

# Test Table
test = Table(
    'test',
    metadata,
    Column('student_id', String, ForeignKey('enrollment_profile.student_id'), primary_key=True),
    Column('test_id', String, ForeignKey('test_metadata.test_id'), primary_key=True),
    Column('subject', Integer, nullable=False),  # 1 to 6
    Column('marks_obtained', Integer, nullable=False)  # -1 if not appeared, 0 to max marks
)

class DatabaseManager:
    def __init__(self, database_url: str = DATABASE_URL):
        self.database_url = database_url
        self.engine: Optional[Engine] = None
    
    def create_engine(self) -> Engine:
        """Create and return SQLAlchemy engine"""
        if self.engine is None:
            self.engine = create_engine(self.database_url)
        return self.engine
    
    def create_tables(self):
        """Create all tables in the database"""
        engine = self.create_engine()
        metadata.create_all(engine)
        print("All tables created successfully!")
    
    def drop_tables(self):
        """Drop all tables in the database"""
        engine = self.create_engine()
        metadata.drop_all(engine)
        print("All tables dropped successfully!")
    
    def get_engine(self) -> Engine:
        """Get the SQLAlchemy engine"""
        if self.engine is None:
            self.create_engine()
        return self.engine
    
    def get_table(self, table_name: str):
        """Get a table object by name"""
        tables = {
            'classes': classes,
            'general_profile': general_profile,
            'enrollment_profile': enrollment_profile,
            'test_metadata': test_metadata,
            'test': test
        }
        return tables.get(table_name)

# Example usage and helper functions
def get_database_manager(database_url: str = DATABASE_URL) -> DatabaseManager:
    """Get a DatabaseManager instance"""
    return DatabaseManager(database_url)

def initialize_database(database_url: str = DATABASE_URL):
    """Initialize the database with all tables"""
    db_manager = get_database_manager(database_url)
    db_manager.create_tables()
    return db_manager

if __name__ == "__main__":
    # Initialize the database
    db_manager = initialize_database()
    
    # Print table information
    print("Database initialized with the following tables:")
    for table in metadata.tables:
        print(f"- {table}")
