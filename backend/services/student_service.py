from typing import List, Optional
from sqlalchemy import text
from datetime import date
from .base_service import BaseService
from ..dto import StudentDTO, EnrollmentDTO
from ..exceptions import ValidationException, NotFoundException, DuplicateResourceException, BusinessRuleException

class StudentService(BaseService):
    """Service for student-related operations"""
    
    def create_student(self, student_dto: StudentDTO, enrollment_dto: EnrollmentDTO) -> StudentDTO:
        """Create a new student with enrollment"""
        # Validate student data
        self._validate_student_data(student_dto)
        
        # Validate enrollment data
        self._validate_enrollment_data(enrollment_dto)
        
        # Check if class exists
        if not self.exists('classes', 'class_id = :class_id', {'class_id': enrollment_dto.class_id}):
            raise NotFoundException(f"Class with ID {enrollment_dto.class_id} not found", "class")
        
        # Check if roll number is unique in the class
        if self.exists('enrollment_profile', 'class_id = :class_id AND roll_no = :roll_no', 
                      {'class_id': enrollment_dto.class_id, 'roll_no': enrollment_dto.roll_no}):
            raise DuplicateResourceException(f"Roll number {enrollment_dto.roll_no} already exists in class", "roll_no")
        
        # Check if admission number is unique
        if self.exists('enrollment_profile', 'admission_no = :admission_no', 
                      {'admission_no': enrollment_dto.admission_no}):
            raise DuplicateResourceException(f"Admission number {enrollment_dto.admission_no} already exists", "admission_no")
        
        # Generate student ID if not provided
        if not student_dto.student_id:
            student_dto.student_id = f"STU_{enrollment_dto.admission_no}"
        
        # Insert enrollment profile first (student_id is primary key)
        enrollment_data = {
            'student_id': student_dto.student_id,
            'class_id': enrollment_dto.class_id,
            'roll_no': enrollment_dto.roll_no,
            'date_of_admission': enrollment_dto.date_of_admission,
            'admission_no': enrollment_dto.admission_no,
            'status_of_previous_academic_year': enrollment_dto.status_of_previous_academic_year
        }
        
        self.execute_insert('enrollment_profile', enrollment_data)
        
        # Insert general profile
        student_data = {
            'student_id': student_dto.student_id,
            'name': student_dto.name,
            'father_name': student_dto.father_name,
            'mother_name': student_dto.mother_name,
            'date_of_birth': student_dto.date_of_birth,
            'gender': student_dto.gender,
            'phone_number': student_dto.phone_number,
            'email': student_dto.email,
            'blood_group': student_dto.blood_group,
            'address': student_dto.address
        }
        
        self.execute_insert('general_profile', student_data)
        
        return student_dto
    
    def get_student_by_id(self, student_id: str) -> StudentDTO:
        """Get a student by ID"""
        result = self.execute_select('general_profile', 'student_id = :student_id', {'student_id': student_id})
        
        if not result:
            raise NotFoundException(f"Student with ID {student_id} not found", "student")
        
        student_data = result[0]
        return StudentDTO(
            student_id=student_data['student_id'],
            name=student_data['name'],
            father_name=student_data['father_name'],
            mother_name=student_data['mother_name'],
            date_of_birth=student_data['date_of_birth'],
            gender=student_data['gender'],
            phone_number=student_data['phone_number'],
            email=student_data['email'],
            blood_group=student_data['blood_group'],
            address=student_data['address']
        )
    
    def get_student_by_roll(self, class_id: str, roll_no: int) -> StudentDTO:
        """Get a student by roll number in a specific class"""
        query = text("""
            SELECT gp.* FROM general_profile gp
            JOIN enrollment_profile ep ON gp.student_id = ep.student_id
            WHERE ep.class_id = :class_id AND ep.roll_no = :roll_no
        """)
        
        result = self.execute_query(query, {'class_id': class_id, 'roll_no': roll_no})
        
        if not result:
            raise NotFoundException(f"Student with roll number {roll_no} not found in class {class_id}", "student")
        
        student_data = dict(result[0]._mapping)
        return StudentDTO(
            student_id=student_data['student_id'],
            name=student_data['name'],
            father_name=student_data['father_name'],
            mother_name=student_data['mother_name'],
            date_of_birth=student_data['date_of_birth'],
            gender=student_data['gender'],
            phone_number=student_data['phone_number'],
            email=student_data['email'],
            blood_group=student_data['blood_group'],
            address=student_data['address']
        )
    
    def get_students_by_class(self, class_id: str) -> List[dict]:
        """Get all students in a class with their details"""
        query = text("""
            SELECT 
                gp.student_id,
                gp.name,
                gp.gender,
                gp.phone_number,
                gp.email,
                ep.roll_no,
                ep.admission_no,
                ep.date_of_admission
            FROM general_profile gp
            JOIN enrollment_profile ep ON gp.student_id = ep.student_id
            WHERE ep.class_id = :class_id
            ORDER BY ep.roll_no
        """)
        
        result = self.execute_query(query, {'class_id': class_id})
        return [dict(row._mapping) for row in result]
    
    def update_student(self, student_id: str, student_dto: StudentDTO) -> StudentDTO:
        """Update student information"""
        # Check if student exists
        existing_student = self.get_student_by_id(student_id)
        
        # Validate student data
        self._validate_student_data(student_dto)
        
        # Update student
        update_data = {
            'name': student_dto.name,
            'father_name': student_dto.father_name,
            'mother_name': student_dto.mother_name,
            'date_of_birth': student_dto.date_of_birth,
            'gender': student_dto.gender,
            'phone_number': student_dto.phone_number,
            'email': student_dto.email,
            'blood_group': student_dto.blood_group,
            'address': student_dto.address
        }
        
        self.execute_update('general_profile', update_data, 'student_id = :student_id', {'student_id': student_id})
        
        return StudentDTO(
            student_id=student_id,
            name=student_dto.name,
            father_name=student_dto.father_name,
            mother_name=student_dto.mother_name,
            date_of_birth=student_dto.date_of_birth,
            gender=student_dto.gender,
            phone_number=student_dto.phone_number,
            email=student_dto.email,
            blood_group=student_dto.blood_group,
            address=student_dto.address
        )
    
    def delete_student(self, student_id: str) -> bool:
        """Delete a student"""
        # Check if student exists
        self.get_student_by_id(student_id)
        
        # Delete from general_profile first (due to foreign key constraint)
        self.execute_delete('general_profile', 'student_id = :student_id', {'student_id': student_id})
        
        # Delete from enrollment_profile
        self.execute_delete('enrollment_profile', 'student_id = :student_id', {'student_id': student_id})
        
        return True
    
    def _validate_student_data(self, student_dto: StudentDTO):
        """Validate student data"""
        if not student_dto.name or len(student_dto.name.strip()) < 2:
            raise ValidationException("Name must be at least 2 characters long", "name")
        
        if student_dto.gender not in ['M', 'F', 'T']:
            raise ValidationException("Gender must be 'M', 'F', or 'T'", "gender")
        
        if student_dto.phone_number and (len(student_dto.phone_number) != 10 or not student_dto.phone_number.isdigit()):
            raise ValidationException("Phone number must be exactly 10 digits", "phone_number")
        
        if student_dto.email and '@' not in student_dto.email:
            raise ValidationException("Invalid email format", "email")
    
    def _validate_enrollment_data(self, enrollment_dto: EnrollmentDTO):
        """Validate enrollment data"""
        if enrollment_dto.roll_no <= 0:
            raise ValidationException("Roll number must be positive", "roll_no")
        
        if enrollment_dto.admission_no <= 0:
            raise ValidationException("Admission number must be positive", "admission_no")
        
        if enrollment_dto.status_of_previous_academic_year not in ['None', 'Self', 'Other']:
            raise ValidationException("Status must be 'None', 'Self', or 'Other'", "status_of_previous_academic_year")
