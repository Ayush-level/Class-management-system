from flask import  request,jsonify,Blueprint
from model import db, Attendance ,student
from datetime import date


student_ID = Blueprint("student", __name__, url_prefix='/api/student')




@student_ID.route('/api/student', methods=["POST"])
def Student_details():
    data=request.get_json()
    required_fields=['name','date_of_birth','gender','father_name','mother_name','date_of_admission' ,'phone_no','address','email']
    
    
    last_student = student.query.order_by(student.roll_number.desc()).first()
    
    if last_student:
        new_roll = last_student.roll_number + 1
    else:
        new_roll = 1



    for field in required_fields:
     if not data.get(field):
      return jsonify({"error":f"Missing {field}"}),400
    
    create_student = student(
        roll_number=new_roll
        name=data['name'],
        date_of_birth=data['date_of_birth'],
        gender=data['gender'],
        father_name=data['father_name'],
        mother_name=data['mother_name'],
        date_of_admission=data['date_of_admission'],
        phone_no=data['phone_no'],
        address=data['address'],
        email=data['email']
    )
    db.session.add(create_student)
    db.session.commit()
    return jsonify({"message":"Student added successfully"}),201

@student_ID.route('/api/student', methods=["GET"])
def get_student():
    students = student.query.all()
    return jsonify([student.to_dict() for student in students])

attendeance_bp = Blueprint("attendeance", __name__, url_prefix='/api/attendeance')

@attendeance_bp.route('/api/attendeance', methods=["POST"])
def Attendance_details():
    data=request.get_json()
    required_fields=['roll_number','date','status']
    
    for field in required_fields:
     if not data.get(field):
      return jsonify({"error":f"Missing {field}"}),400


    
    
    create_attendance = Attendance(
        roll_number=data['roll_number'],
        date=data['date'],
        status=data['status']
    )
    attendance_date = data.get('date', str(date.today()))

    existing = Attendance.query.filter_by(roll_number=data['roll_number'], date=attendance_date).first()
    if existing:
        return jsonify({"error": "Attendance already marked for this student on this date"}), 400
   

    new_attendance = Attendance(
        roll_number=data['roll_number'],
        date=attendance_date,
        status=data['status'].capitalize()
       )
   
    db.session.add(new_attendance)
    db.session.commit()
    return jsonify({"message":"Attendance added successfully"}),201

@attendeance_bp.route('/api/attendeance', methods=["GET"])
def get_attendance():
    attendances = Attendance.query.all()
    return jsonify([attendance.to_dict() for attendance in attendances])

@attendance_know.route('/api/attendance/date/<string:attendance_date>', methods=['GET'])
def get_attendance_for_date(attendance_date):
    records = Attendance.query.filter_by(date=attendance_date).all()
    return jsonify([record.to_dict() for record in records])


if __name__ == "__main__":
    app.run(debug=True)
