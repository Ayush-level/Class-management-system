from flask import request,jsonify,Blueprint
from datetime import datetime
from models import Attendance,Student,db
from models.school_class import SchoolClass
from models.db import db


attendance_bp = Blueprint("attendance", __name__) 

@attendance_bp.route("/classes/<int:class_id>/attendance", methods=["GET"])
def get_students(class_id):

    students = Student.query.filter_by(class_id=class_id).all()

    data = []

    for s in students:
        data.append({
            "roll": s.roll,
            "name": s.name,
            "gender": s.gender
        })

    return jsonify(data)

@attendance_bp.route('/classes/<int:class_id>/api/attendance', methods=["POST"]) #this is a API endpoint for students attendeance
def Attendance_details(class_id):
    data=request.get_json()
    required_fields=['roll_number','date','status']
    
    for field in required_fields:                               # Check if this field exists in data, Check if ALL fields are present
        if field not in data:# Check if NOT all fields are present
            return jsonify({"error":f"Missing {field}"}),400

    allowed_status = ["Present", "Absent"]
    status=data['status'].capitalize()

    if  status not in allowed_status:
        return jsonify({"error":"Invalid status"}),400  

    student = Student.query.filter_by(roll=data['roll_number']).first()
    if not student:
        return jsonify({"error":"Student not found"}),404

    attendece_data = data.get('date')
   
    if attendance_date:
        attendance_date = datetime.strptime(
            attendance_date, "%Y-%m-%d"
        ).date()
    else:
        attendance_date = datetime.utcnow().date()


    new_attendance = Attendance(
        roll_number=student.roll,
        date=attendance_date,
        status=status
    )
    
    
   
   
    db.session.add(new_attendance)
    db.session.commit()
    return jsonify({"message":"Attendance added successfully"}),201

@attendance_bp.route('/classes/<int:class_id>/attendance', methods=["GET"])
def get_attendance(class_id):

    attendance_date = request.args.get("date")

    query = Attendance.query.join(Student).filter(Student.class_id==class_id) 

    if attendance_date:
       
        
        try:
            attendance_date = datetime.strptime(
                attendance_date, "%Y-%m-%d"
            ).date()

            query = query.filter(Attendance.date==attendance_date)

        except ValueError:
            return jsonify({"error": "Use YYYY-MM-DD"}), 400

    records = query.all()

    return jsonify([record.to_dict() for record in records])
