from flask import request,jsonify,Blueprint
from datetime import datetime
from models import Attendance,Student,db
attendance_bp = Blueprint("attendance", __name__) 

@attendance_bp.route("/attendance", methods=["GET"])
def dashboard():

    students = Student.query.all()

    data = []

    for s in students:
        data.append({
            "roll": s.roll,
            "name": s.name,
            "gender": s.gender
        })

    return jsonify(data)

@attendance_bp.route('/api/attendance', methods=["POST"]) #this is a API endpoint for students attendeance
def Attendance_details():
    data=request.get_json()
    required_fields=['roll_number','date','status']
    
    for field in required_fields:                               # Check if this field exists in data, Check if ALL fields are present
        if field not in data:# Check if NOT all fields are present
            return jsonify({"error":f"Missing {field}"}),400

  

    new_attendance = Attendance(
        roll_number=data['roll_number'],
        date=data['date'],
        allowed_status = ["Present", "Absent"],
        status=data['status'].capitalize()
       )
    
    if data['status'] not in allowed_status:
        return jsonify({"error":"Invalid status"}),400
   
    db.session.add(new_attendance)
    db.session.commit()
    return jsonify({"message":"Attendance added successfully"}),201

@attendance_bp.route('/attendance', methods=["GET"])
def get_attendance():

    attendance_date = request.args.get("date")

    query = Attendance.query

    if attendance_date:
       
        
        try:
            attendance_date = datetime.strptime(
                attendance_date, "%Y-%m-%d"
            ).date()

            query = query.filter_by(date=attendance_date)

        except ValueError:
            return jsonify({"error": "Use YYYY-MM-DD"}), 400

    records = query.all()

    return jsonify([record.to_dict() for record in records])
