from flask import request,jsonify,Blueprint
from datetime import date
from services import attendance_service, student_service
from dto import AttendanceDTO
from exceptions import ServiceException, NotFoundException, ValidationException

attendance_bp = Blueprint("attendance", __name__) 

@attendance_bp.route("/classes/<class_id>/attendance", methods=["GET"])
def get_class_attendance(class_id):
    try:
        # Get date from query parameters
        attendance_date_str = request.args.get('date')
        if not attendance_date_str:
            attendance_date = date.today()
        else:
            attendance_date = date.fromisoformat(attendance_date_str)
        
        # Get attendance for the class
        attendance_data = attendance_service.get_attendance_by_class(class_id, attendance_date)
        
        return jsonify({
            'date': attendance_date.isoformat(),
            'class_id': class_id,
            'attendance': attendance_data
        })
    
    except NotFoundException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 404
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@attendance_bp.route('/classes/<class_id>/attendance', methods=["POST"])
def mark_class_attendance(class_id):
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'date' not in data:
            return jsonify({"error": "Missing date field"}), 400
        if 'attendance' not in data:
            return jsonify({"error": "Missing attendance field"}), 400
        
        attendance_date = date.fromisoformat(data['date']) if isinstance(data['date'], str) else data['date']
        attendance_records = data['attendance']
        
        # Mark bulk attendance
        results = attendance_service.mark_bulk_attendance(class_id, attendance_date, attendance_records)
        
        return jsonify({
            "message": f"Attendance marked for {len(results)} students",
            "date": attendance_date.isoformat(),
            "marked_count": len(results)
        }), 201
    
    except ValidationException as e:
        return jsonify({"error": e.message, "field": e.field, "error_code": e.error_code}), 400
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@attendance_bp.route('/classes/<class_id>/students/<student_id>/attendance', methods=["POST"])
def mark_student_attendance(class_id, student_id):
    try:
        data = request.get_json()
        required_fields = ['date', 'status']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing {field} field"}), 400

        # Create attendance DTO
        attendance_dto = AttendanceDTO(
            student_id=student_id,
            date=date.fromisoformat(data['date']) if isinstance(data['date'], str) else data['date'],
            status=data['status'].capitalize()
        )

        # Mark attendance
        result = attendance_service.mark_attendance(attendance_dto)

        return jsonify({
            "message": "Attendance marked successfully",
            "student_id": result.student_id,
            "date": result.date.isoformat(),
            "status": result.status
        }), 201

    except ValidationException as e:
        return jsonify({"error": e.message, "field": e.field, "error_code": e.error_code}), 400
    except NotFoundException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 404
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@attendance_bp.route('/classes/<class_id>/students/<student_id>/attendance', methods=["GET"])
def get_student_attendance(class_id, student_id):
    try:
        # Get date range from query parameters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None
        
        # Get attendance records
        attendance_records = attendance_service.get_attendance_by_student(student_id, start_date, end_date)
        
        return jsonify({
            'student_id': student_id,
            'attendance': [att.to_dict() for att in attendance_records]
        })
    
    except NotFoundException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 404
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@attendance_bp.route('/classes/<class_id>/students/<student_id>/attendance/statistics', methods=["GET"])
def get_student_attendance_statistics(class_id, student_id):
    try:
        # Get date range from query parameters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        if not start_date_str or not end_date_str:
            return jsonify({"error": "Both start_date and end_date are required"}), 400
        
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
        
        # Get attendance statistics
        stats = attendance_service.get_attendance_statistics(student_id, start_date, end_date)
        
        return jsonify({
            'student_id': student_id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'statistics': stats
        })
    
    except NotFoundException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 404
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
