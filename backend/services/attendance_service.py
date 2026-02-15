from typing import List, Optional
from sqlalchemy import text
from datetime import date
from .base_service import BaseService
from ..dto import AttendanceDTO
from ..exceptions import ValidationException, NotFoundException

class AttendanceService(BaseService):
    """Service for attendance-related operations"""
    
    def mark_attendance(self, attendance_dto: AttendanceDTO) -> AttendanceDTO:
        """Mark attendance for a student"""
        # Validate attendance data
        self._validate_attendance_data(attendance_dto)
        
        # Check if student exists
        if not self.exists('general_profile', 'student_id = :student_id', {'student_id': attendance_dto.student_id}):
            raise NotFoundException(f"Student with ID {attendance_dto.student_id} not found", "student")
        
        # Check if attendance already exists for this student on this date
        if self.exists('attendance', 'student_id = :student_id AND date = :date', 
                      {'student_id': attendance_dto.student_id, 'date': attendance_dto.date}):
            # Update existing attendance
            self.execute_update('attendance', 
                               {'status': attendance_dto.status},
                               'student_id = :student_id AND date = :date',
                               {'student_id': attendance_dto.student_id, 'date': attendance_dto.date})
        else:
            # Insert new attendance
            attendance_data = {
                'student_id': attendance_dto.student_id,
                'date': attendance_dto.date,
                'status': attendance_dto.status
            }
            self.execute_insert('attendance', attendance_data)
        
        return attendance_dto
    
    def get_attendance_by_student(self, student_id: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[AttendanceDTO]:
        """Get attendance records for a student"""
        where_clause = 'student_id = :student_id'
        params = {'student_id': student_id}
        
        if start_date and end_date:
            where_clause += ' AND date BETWEEN :start_date AND :end_date'
            params['start_date'] = start_date
            params['end_date'] = end_date
        elif start_date:
            where_clause += ' AND date >= :start_date'
            params['start_date'] = start_date
        elif end_date:
            where_clause += ' AND date <= :end_date'
            params['end_date'] = end_date
        
        result = self.execute_select('attendance', where_clause, params)
        
        attendances = []
        for attendance_data in result:
            attendances.append(AttendanceDTO(
                student_id=attendance_data['student_id'],
                date=attendance_data['date'],
                status=attendance_data['status']
            ))
        
        return attendances
    
    def get_attendance_by_class(self, class_id: str, attendance_date: date) -> List[dict]:
        """Get attendance for all students in a class on a specific date"""
        query = text("""
            SELECT 
                gp.student_id,
                gp.name,
                gp.roll_no,
                COALESCE(a.status, 'Not Marked') as status
            FROM enrollment_profile ep
            JOIN general_profile gp ON ep.student_id = gp.student_id
            LEFT JOIN attendance a ON gp.student_id = a.student_id AND a.date = :attendance_date
            WHERE ep.class_id = :class_id
            ORDER BY ep.roll_no
        """)
        
        result = self.execute_query(query, {'class_id': class_id, 'attendance_date': attendance_date})
        return [dict(row._mapping) for row in result]
    
    def get_attendance_statistics(self, student_id: str, start_date: date, end_date: date) -> dict:
        """Get attendance statistics for a student in a date range"""
        query = text("""
            SELECT 
                COUNT(*) as total_days,
                COUNT(CASE WHEN status = 'Present' THEN 1 END) as present_days,
                COUNT(CASE WHEN status = 'Absent' THEN 1 END) as absent_days,
                COUNT(CASE WHEN status = 'Not Marked' THEN 1 END) as not_marked_days
            FROM (
                SELECT 
                    gp.student_id,
                    COALESCE(a.status, 'Not Marked') as status,
                    d.date
                FROM enrollment_profile ep
                JOIN general_profile gp ON ep.student_id = ep.student_id
                CROSS JOIN (
                    SELECT DATE(:start_date) + INTERVAL seq DAY as date
                    FROM (
                        SELECT 0 as seq UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
                        UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9
                    ) numbers
                    WHERE DATE(:start_date) + INTERVAL seq DAY <= DATE(:end_date)
                ) d
                LEFT JOIN attendance a ON gp.student_id = a.student_id AND a.date = d.date
                WHERE gp.student_id = :student_id
            ) attendance_data
        """)
        
        result = self.execute_query(query, {
            'student_id': student_id, 
            'start_date': start_date, 
            'end_date': end_date
        })
        
        stats = dict(result[0]._mapping)
        total_days = stats['total_days']
        
        if total_days > 0:
            attendance_percentage = (stats['present_days'] / total_days) * 100
        else:
            attendance_percentage = 0
        
        return {
            'total_days': total_days,
            'present_days': stats['present_days'],
            'absent_days': stats['absent_days'],
            'not_marked_days': stats['not_marked_days'],
            'attendance_percentage': round(attendance_percentage, 2)
        }
    
    def mark_bulk_attendance(self, class_id: str, attendance_date: date, attendance_data: List[dict]) -> List[AttendanceDTO]:
        """Mark attendance for multiple students in a class"""
        results = []
        
        for attendance_record in attendance_data:
            try:
                attendance_dto = AttendanceDTO(
                    student_id=attendance_record['student_id'],
                    date=attendance_date,
                    status=attendance_record['status']
                )
                
                result = self.mark_attendance(attendance_dto)
                results.append(result)
                
            except Exception as e:
                # Log error but continue with other students
                print(f"Error marking attendance for student {attendance_record.get('student_id', 'unknown')}: {e}")
        
        return results
    
    def _validate_attendance_data(self, attendance_dto: AttendanceDTO):
        """Validate attendance data"""
        if attendance_dto.status not in ['Present', 'Absent']:
            raise ValidationException("Status must be 'Present' or 'Absent'", "status")
