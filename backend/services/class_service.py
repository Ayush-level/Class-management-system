from typing import List, Optional
from sqlalchemy import text
from .base_service import BaseService
from ..dto import ClassDTO
from ..exceptions import ValidationException, NotFoundException, DuplicateResourceException

class ClassService(BaseService):
    """Service for class-related operations"""
    
    def create_class(self, class_dto: ClassDTO) -> ClassDTO:
        """Create a new class"""
        # Validate class level
        if not 1 <= class_dto.class_level <= 5:
            raise ValidationException("Class level must be between 1 and 5", "class_level")
        
        # Check if class already exists
        if self.exists('classes', 'class_id = :class_id', {'class_id': class_dto.class_id}):
            raise DuplicateResourceException(f"Class with ID {class_dto.class_id} already exists", "class")
        
        # Insert class
        class_data = {
            'class_id': class_dto.class_id,
            'class': class_dto.class_level,
            'section': class_dto.section
        }
        
        self.execute_insert('classes', class_data)
        return class_dto
    
    def get_class_by_id(self, class_id: str) -> ClassDTO:
        """Get a class by ID"""
        result = self.execute_select('classes', 'class_id = :class_id', {'class_id': class_id})
        
        if not result:
            raise NotFoundException(f"Class with ID {class_id} not found", "class")
        
        class_data = result[0]
        return ClassDTO(
            class_id=class_data['class_id'],
            class_level=class_data['class'],
            section=class_data['section']
        )
    
    def get_all_classes(self) -> List[ClassDTO]:
        """Get all classes"""
        result = self.execute_select('classes')
        
        classes = []
        for class_data in result:
            classes.append(ClassDTO(
                class_id=class_data['class_id'],
                class_level=class_data['class'],
                section=class_data['section']
            ))
        
        return classes
    
    def update_class(self, class_id: str, class_dto: ClassDTO) -> ClassDTO: #To be reviewed
        """Update a class"""
        # Check if class exists
        if not self.exists('classes', 'class_id = :class_id', {'class_id': class_dto.class_id}):
            raise NotFoundException(f"Class with ID {class_id} not found", "class")
        
        # Validate class level
        if not 1 <= class_dto.class_level <= 5:
            raise ValidationException("Class level must be between 1 and 5", "class_level")
        
        # Update class
        update_data = {
            'class': class_dto.class_level,
            'section': class_dto.section
        }
        
        self.execute_update('classes', update_data, 'class_id = :class_id', {'class_id': class_id})
        
        return ClassDTO(
            class_id=class_id,
            class_level=class_dto.class_level,
            section=class_dto.section
        )
    
    def delete_class(self, class_id: str) -> bool:
        """Delete a class"""
        # Check if class exists
        if not self.exists('classes', 'class_id = :class_id', {'class_id': class_id}):
            raise NotFoundException(f"Class with ID {class_id} not found", "class")
        
        # Check if class has enrolled students
        if self.exists('enrollment_profile', 'class_id = :class_id', {'class_id': class_id}):
            raise ValidationException("Cannot delete class with enrolled students", "class_id")
        
        # Delete class
        self.execute_delete('classes', 'class_id = :class_id', {'class_id': class_id})
        return True
    
    def get_students_in_class(self, class_id: str) -> List[dict]:
        """Get all students in a class with their enrollment details"""
        query = text("""
            SELECT 
                gp.student_id,
                gp.name,
                gp.gender,
                ep.roll_no,
                ep.admission_no
            FROM general_profile gp
            JOIN enrollment_profile ep ON gp.student_id = ep.student_id
            WHERE ep.class_id = :class_id
            ORDER BY ep.roll_no
        """)
        
        result = self.execute_query(query, {'class_id': class_id})
        return [dict(row._mapping) for row in result]
