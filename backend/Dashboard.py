from flask import request,jsonify,Blueprint
from datetime import date
from services import student_service, class_service, enrollment_service
from dto import StudentDTO, EnrollmentDTO
from exceptions import ServiceException, NotFoundException, ValidationException

student_bp = Blueprint("student", __name__)

@student_bp.route("/classes/<class_id>/students", methods=["GET"])
def dashboard(class_id):
    try:
        # Check if class exists
        class_service.get_class_by_id(class_id)
        
        # Get students in class
        students = student_service.get_students_by_class(class_id)
        
        data = []
        for s in students:
            data.append({
                "id": s['student_id'],
                "roll": s['roll_no'],
                "name": s['name'],
                "gender": s['gender'],
                "gp_url": f"/classes/{class_id}/students/{s['student_id']}",
                "ep_url": f"/classes/{class_id}/students/{s['student_id']}/enrollment"
            })

        return jsonify(data)
    
    except NotFoundException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 404
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@student_bp.route("/classes/<class_id>/add_student", methods=["POST"]) 
def Student_details(class_id):
    try:
        # Check if class exists
        class_service.get_class_by_id(class_id)
        
        data = request.get_json()
        required_fields = ['name', 'date_of_birth', 'gender', 'father_name', 'mother_name', 
                          'phone_no', 'address', 'email', 'blood_group', 'roll', 
                          'admission_no', 'date_of_admission', 'status_of_previous_academic_year']

        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing {field}"}), 400

        # Create student DTO
        student_dto = StudentDTO(
            name=data['name'],
            date_of_birth=date.fromisoformat(data['date_of_birth']) if isinstance(data['date_of_birth'], str) else data['date_of_birth'],
            gender=data['gender'],
            father_name=data['father_name'],
            mother_name=data['mother_name'],
            phone_number=data['phone_no'],
            address=data['address'],
            email=data['email'],
            blood_group=data['blood_group']
        )

        # Create enrollment DTO
        enrollment_dto = EnrollmentDTO(
            student_id="",  # Will be generated
            class_id=class_id,
            roll_no=data['roll'],
            date_of_admission=date.fromisoformat(data['date_of_admission']) if isinstance(data['date_of_admission'], str) else data['date_of_admission'],
            admission_no=data['admission_no'],
            status_of_previous_academic_year=data['status_of_previous_academic_year']
        )

        # Create student
        created_student = student_service.create_student(student_dto, enrollment_dto)

        return jsonify({
            "message": "Student added successfully",
            "student_id": created_student.student_id,
            "next_url": f"/classes/{class_id}/students/{created_student.student_id}/enrollment"
        }), 201

    except ValidationException as e:
        return jsonify({"error": e.message, "field": e.field, "error_code": e.error_code}), 400
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@student_bp.route("/classes/<class_id>/students/<student_id>/enrollment", methods=["POST"])
def add_enrollment(class_id, student_id):
    try:
        # This endpoint might not be needed since enrollment is created with student
        # But keeping for backward compatibility
        student = student_service.get_student_by_id(student_id)
        
        data = request.json
        
        enrollment_dto = EnrollmentDTO(
            student_id=student_id,
            class_id=class_id,
            roll_no=data.get("roll_no", 1),
            date_of_admission=date.fromisoformat(data['date_of_admission']) if isinstance(data['date_of_admission'], str) else data['date_of_admission'],
            admission_no=data["admission_no"],
            status_of_previous_academic_year=data.get("status_of_previous_academic_year", "None")
        )

        enrollment_service.create_enrollment(enrollment_dto)

        return jsonify({
            "message": "Student fully onboarded",
            "dashboard_url": f"/classes/{class_id}/students"
        }), 201

    except NotFoundException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 404
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@student_bp.route("/classes/<class_id>/students/<student_id>", methods=["GET"]) 
def get_student(class_id, student_id):
    try:
        # Get student details
        student = student_service.get_student_by_id(student_id)
        
        # Get enrollment details
        enrollments = enrollment_service.get_enrollment_by_student(student_id)
        current_enrollment = next((e for e in enrollments if e.class_id == class_id), None)
        
        if not current_enrollment:
            return jsonify({"error": "Student not found in this class"}), 404

        return jsonify({
            "name": student.name,
            "roll": current_enrollment.roll_no,
            "email": student.email,
            "phone_no": student.phone_number,
            "father_name": student.father_name,
            "mother_name": student.mother_name,
            "date_of_admission": current_enrollment.date_of_admission.isoformat(),
            "date_of_birth": student.date_of_birth.isoformat() if student.date_of_birth else None,
            "address": student.address,
            "gender": student.gender,
            "blood_group": student.blood_group,
            "class_id": current_enrollment.class_id,
            "student_id": student.student_id
        }), 200
    
    except NotFoundException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 404
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
