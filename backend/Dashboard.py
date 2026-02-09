from flask import request,jsonify,Blueprint
from datetime import date
from models.school_class import SchoolClass
from models.student import Student
from models.enrollment import Enrollment
from models.db import db

student_bp = Blueprint("student", __name__)

@student_bp.route("/classes/<int:class_id>/students", methods=["GET"])
def dashboard(class_id):

    school_class = SchoolClass.query.get_or_404(class_id)
    students = school_class.students

    data = []

    for s in students:
        data.append({
            "id": s.id,
            "roll": s.roll,
            "name": s.name,
            "gender": s.gender,
            "gp_url": f"/classes/{class_id}/students/{s.id}",
            "ep_url": f"/classes/{class_id}/students/{s.id}/enrollment"
        })

    return jsonify(data)





 # All URLs in this file start with `/api/students`



@student_bp.route("/classes/<int:class_id>/add_student", methods=["POST"]) 
def Student_details(class_id):
    SchoolClass.query.get_or_404(class_id)
    data=request.get_json() 
    required_fields=['name','date_of_birth','gender','father_name','mother_name','phone_no','address','email','blood_group','roll']
    # A list of required fields





    for field in required_fields:
       if field not in data:# Check if NOT all fields are present
           return jsonify({"error":f"Missing {field}"}),400
    
    create_student = Student(
       
        name=data['name'],
        date_of_birth=data['date_of_birth'],
        gender=data['gender'],
        father_name=data['father_name'],
        mother_name=data['mother_name'],
       
        phone_no=data['phone_no'],
        address=data['address'],
        email=data['email'],
        blood_group=data['blood_group'],
        roll=data['roll'],
        class_id=class_id
    )
    db.session.add(create_student) # Add student to database session
    db.session.commit()
    return jsonify({"message":"Student added successfully",
    "student_id": create_student.id,
    "next_url": f"/classes/{class_id}/students/{create_student.id}/enrollment"}),201


@student_bp.route("/classes/<int:class_id>/students/<int:id>/enrollment", methods=["POST"])
def add_enrollment(class_id,id):

    student = Student.query.get_or_404(id)

    data = request.json

    enrollment = Enrollment(
        enrollment_number=data["enrollment_number"],
        Medium_of_Instruction=data["Medium_of_Instruction"],
        Status_of_student_in_Previous_Academic_Year_of_Schooling=data["Status_of_student_in_Previous_Academic_Year_of_Schooling"],
        date_of_admission=data['date_of_admission'],
        student=student
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        "message": "Student fully onboarded",
        "dashboard_url": "/classes/{class_id}/students"
    }), 201



@student_bp.route("/classes/<int:class_id>/students/<int:student_rlno>", methods=["GET"]) 
def get_student(class_id,student_rlno):
    students = Student.query.get(student_rlno)

    if not students:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "name": student.name,
        "roll": student.roll,
        "email": student.email,
        "phone_no": student.phone_no,
        "father_name": student.father_name,
        "mother_name": student.mother_name,
        "date_of_admission": student.date_of_admission,
        "date_of_birth": student.date_of_birth,
        "address": student.address,
        "gender":student.gender,
        "blood_group":student.blood_group,
        "roll":student.roll,
        "class_id":student.class_id,
        "student_id":students.id
    }),200
    

