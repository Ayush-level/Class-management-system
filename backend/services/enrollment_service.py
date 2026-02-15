from typing import List, Optional
from sqlalchemy import text
from datetime import date
from .base_service import BaseService
from ..dto import EnrollmentDTO
from ..exceptions import ValidationException, NotFoundException, DuplicateResourceException

class EnrollmentService(BaseService):
    """Service for enrollment-related operations"""
    
    def create_enrollment(self, enrollment_dto: EnrollmentDTO) -> EnrollmentDTO:
        """Create a new enrollment"""
        # Validate enrollment data
        self._validate_enrollment_data(enrollment_dto)
        
        # Check if student exists
        if not self.exists('general_profile', 'student_id = :student_id', {'student_id': enrollment_dto.student_id}):
            raise NotFoundException(f"Student with ID {enrollment_dto.student_id} not found", "student")
        
        # Check if class exists
        if not self.exists('classes', 'class_id = :class_id', {'class_id': enrollment_dto.class_id}):
            raise NotFoundException(f"Class with ID {enrollment_dto.class_id} not found", "class")
        
        # Check if student is already enrolled in this class
        if self.exists('enrollment_profile', 'student_id = :student_id AND class_id = :class_id', 
                      {'student_id': enrollment_dto.student_id, 'class_id': enrollment_dto.class_id}):
            raise DuplicateResourceException("Student is already enrolled in this class", "enrollment")
        
        # Check if roll number is unique in the class
        if self.exists('enrollment_profile', 'class_id = :class_id AND roll_no = :roll_no', 
                      {'class_id': enrollment_dto.class_id, 'roll_no': enrollment_dto.roll_no}):
            raise DuplicateResourceException(f"Roll number {enrollment_dto.roll_no} already exists in class", "roll_no")
        
        # Check if admission number is unique
        if self.exists('enrollment_profile', 'admission_no = :admission_no', 
                      {'admission_no': enrollment_dto.admission_no}):
            raise DuplicateResourceException(f"Admission number {enrollment_dto.admission_no} already exists", "admission_no")
        
        # Insert enrollment
        enrollment_data = {
            'student_id': enrollment_dto.student_id,
            'class_id': enrollment_dto.class_id,
            'roll_no': enrollment_dto.roll_no,
            'date_of_admission': enrollment_dto.date_of_admission,
            'admission_no': enrollment_dto.admission_no,
            'status_of_previous_academic_year': enrollment_dto.status_of_previous_academic_year
        }
        
        self.execute_insert('enrollment_profile', enrollment_data)
        return enrollment_dto
    
    def get_enrollment_by_student(self, student_id: str) -> List[EnrollmentDTO]:
        """Get all enrollments for a student"""
        result = self.execute_select('enrollment_profile', 'student_id = :student_id', {'student_id': student_id})
        
        enrollments = []
        for enrollment_data in result:
            enrollments.append(EnrollmentDTO(
                student_id=enrollment_data['student_id'],
                class_id=enrollment_data['class_id'],
                roll_no=enrollment_data['roll_no'],
                date_of_admission=enrollment_data['date_of_admission'],
                admission_no=enrollment_data['admission_no'],
                status_of_previous_academic_year=enrollment_data['status_of_previous_academic_year']
            ))
        
        return enrollments
    
    def get_enrollment_by_class(self, class_id: str) -> List[dict]:
        """Get all enrollments in a class with student details"""
        query = text("""
            SELECT 
                ep.student_id,
                ep.roll_no,
                ep.admission_no,
                ep.date_of_admission,
                ep.status_of_previous_academic_year,
                gp.name,
                gp.gender
            FROM enrollment_profile ep
            JOIN general_profile gp ON ep.student_id = gp.student_id
            WHERE ep.class_id = :class_id
            ORDER BY ep.roll_no
        """)
        
        result = self.execute_query(query, {'class_id': class_id})
        return [dict(row._mapping) for row in result]
    
    def update_enrollment(self, student_id: str, class_id: str, enrollment_dto: EnrollmentDTO) -> EnrollmentDTO:
        """Update enrollment information"""
        # Check if enrollment exists
        if not self.exists('enrollment_profile', 'student_id = :student_id AND class_id = :class_id', 
                          {'student_id': student_id, 'class_id': class_id}):
            raise NotFoundException("Enrollment not found", "enrollment")
        
        # Validate enrollment data
        self._validate_enrollment_data(enrollment_dto)
        
        # Check if new roll number conflicts with other students
        if enrollment_dto.roll_no != self._get_current_roll_no(student_id, class_id):
            if self.exists('enrollment_profile', 'class_id = :class_id AND roll_no = :roll_no AND student_id != :student_id', 
                          {'class_id': class_id, 'roll_no': enrollment_dto.roll_no, 'student_id': student_id}):
                raise DuplicateResourceException(f"Roll number {enrollment_dto.roll_no} already exists in class", "roll_no")
        
        # Update enrollment
        update_data = {
            'roll_no': enrollment_dto.roll_no,
            'date_of_admission': enrollment_dto.date_of_admission,
            'admission_no': enrollment_dto.admission_no,
            'status_of_previous_academic_year': enrollment_dto.status_of_previous_academic_year
        }
        
        self.execute_update('enrollment_profile', update_data, 
                           'student_id = :student_id AND class_id = :class_id', 
                           {'student_id': student_id, 'class_id': class_id})
        
        return enrollment_dto
    
    def delete_enrollment(self, student_id: str, class_id: str) -> bool:
        """Delete an enrollment"""
        # Check if enrollment exists
        if not self.exists('enrollment_profile', 'student_id = :student_id AND class_id = :class_id', 
                          {'student_id': student_id, 'class_id': class_id}):
            raise NotFoundException("Enrollment not found", "enrollment")
        
        # Delete enrollment
        self.execute_delete('enrollment_profile', 'student_id = :student_id AND class_id = :class_id', 
                           {'student_id': student_id, 'class_id': class_id})
        
        return True
    
    def get_class_statistics(self, class_id: str) -> dict:
        """Get enrollment statistics for a class"""
        query = text("""
            SELECT 
                COUNT(*) as total_students,
                COUNT(CASE WHEN gp.gender = 'M' THEN 1 END) as male_students,
                COUNT(CASE WHEN gp.gender = 'F' THEN 1 END) as female_students,
                COUNT(CASE WHEN gp.gender = 'T' THEN 1 END) as transgender_students
            FROM enrollment_profile ep
            JOIN general_profile gp ON ep.student_id = gp.student_id
            WHERE ep.class_id = :class_id
        """)
        
        result = self.execute_query(query, {'class_id': class_id})
        stats = dict(result[0]._mapping)
        
        return {
            'total_students': stats['total_students'],
            'male_students': stats['male_students'],
            'female_students': stats['female_students'],
            'transgender_students': stats['transgender_students']
        }
    
    def _validate_enrollment_data(self, enrollment_dto: EnrollmentDTO):
        """Validate enrollment data"""
        if enrollment_dto.roll_no <= 0:
            raise ValidationException("Roll number must be positive", "roll_no")
        
        if enrollment_dto.admission_no <= 0:
            raise ValidationException("Admission number must be positive", "admission_no")
        
        if enrollment_dto.status_of_previous_academic_year not in ['None', 'Self', 'Other']:
            raise ValidationException("Status must be 'None', 'Self', or 'Other'", "status_of_previous_academic_year")
    
    def _get_current_roll_no(self, student_id: str, class_id: str) -> int:
        """Get current roll number for a student in a class"""
        result = self.execute_select('enrollment_profile', 'student_id = :student_id AND class_id = :class_id', 
                                    {'student_id': student_id, 'class_id': class_id})
        
        if result:
            return result[0]['roll_no']
        return 0
