"""Service layer initialization"""

from .class_service import ClassService
from .student_service import StudentService
from .enrollment_service import EnrollmentService
from .base_service import BaseService

# Service instances for dependency injection
class_service = ClassService()
student_service = StudentService()
enrollment_service = EnrollmentService()

__all__ = [
    'BaseService',
    'ClassService', 
    'StudentService', 
    'EnrollmentService',
    'class_service',
    'student_service', 
    'enrollment_service'
]
