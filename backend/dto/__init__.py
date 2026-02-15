"""Data Transfer Objects for the service layer"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import date, datetime

@dataclass
class ClassDTO:
    """Class data transfer object"""
    class_id: str
    class_level: int
    section: str
    
    def to_dict(self) -> dict:
        return {
            'class_id': self.class_id,
            'class': self.class_level,
            'section': self.section
        }

@dataclass
class StudentDTO:
    """Student data transfer object"""
    student_id: Optional[str] = None
    name: str = ""
    father_name: str = ""
    mother_name: str = ""
    date_of_birth: Optional[date] = None
    gender: str = ""
    phone_number: str = ""
    email: str = ""
    blood_group: str = ""
    address: str = ""
    
    def to_dict(self) -> dict:
        return {
            'student_id': self.student_id,
            'name': self.name,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'email': self.email,
            'blood_group': self.blood_group,
            'address': self.address
        }

@dataclass
class EnrollmentDTO:
    """Enrollment data transfer object"""
    student_id: str
    class_id: str
    roll_no: int
    date_of_admission: date
    admission_no: int
    status_of_previous_academic_year: str
    
    def to_dict(self) -> dict:
        return {
            'student_id': self.student_id,
            'class_id': self.class_id,
            'roll_no': self.roll_no,
            'date_of_admission': self.date_of_admission.isoformat(),
            'admission_no': self.admission_no,
            'status_of_previous_academic_year': self.status_of_previous_academic_year
        }

@dataclass
class TestMetadataDTO:
    """Test metadata data transfer object"""
    test_id: str
    test_name: str
    test_date: date
    subjects: List[dict]  # List of {'subject': str, 'max_marks': int}
    
    def to_dict(self) -> dict:
        return {
            'test_id': self.test_id,
            'test_name': self.test_name,
            'test_date': self.test_date.isoformat(),
            'subjects': self.subjects
        }

@dataclass
class TestResultDTO:
    """Test result data transfer object"""
    student_id: str
    test_id: str
    subject: int
    marks_obtained: int
    
    def to_dict(self) -> dict:
        return {
            'student_id': self.student_id,
            'test_id': self.test_id,
            'subject': self.subject,
            'marks_obtained': self.marks_obtained
        }

@dataclass
class AttendanceDTO:
    """Attendance data transfer object"""
    student_id: str
    date: date
    status: str  # "Present" or "Absent"
    
    def to_dict(self) -> dict:
        return {
            'student_id': self.student_id,
            'date': self.date.isoformat(),
            'status': self.status
        }
