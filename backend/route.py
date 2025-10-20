from flask import  request,jsonify,Blueprint
from model import db, Attendance ,student # model is file which Raj will make define what a Student looks like in the database
from datetime import date


student_ID = Blueprint("student", __name__, url_prefix='/api/student') # All URLs in this file start with `/api/students`



@student_ID.route('/api/student', methods=["POST"]) # this is a API endpiont. 
def Student_details():
    data=request.get_json() # the data Frontend sent and Converts it to Python dictionary .
    required_fields=['name','date_of_birth','gender','father_name','mother_name','date_of_admission' ,'phone_no','address','email']
    # A list of required fields

    roll_number = 
    
    last_student = student.query.order_by(student.roll_number.desc()).first()# store roll number in sequece as student add
    
    if last_student:
        new_roll = last_student.roll_number + 1
    else:
        new_roll = 1



    for field in required_fields:
     if not data.get(field):    # Check if NOT all fields are present
      return jsonify({"error":f"Missing {field}"}),400
    
    create_student = student(
        roll_number=new_roll,
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
    db.session.add(create_student) # Add student to database session
    db.session.commit()
    return jsonify({"message":"Student added successfully"}),201

@student_ID.route('/api/student', methods=["GET"]) 
def get_student():
    students = student.query.all()
    return jsonify([student.to_dict() for student in students])

attendeance_bp = Blueprint("attendeance", __name__, url_prefix='/api/attendeance') 

@attendeance_bp.route('/api/attendeance', methods=["POST"]) #this is a API endpoint for students attendeance
def Attendance_details():
    data=request.get_json()
    required_fields=['roll_number','date','status']
    
    for field in required_fields:                               # Check if this field exists in data, Check if ALL fields are present
     if not data.get(field):                                                         # Check if NOT all fields are present 
      return jsonify({"error":f"Missing {field}"}),400


    
    
    create_attendance = Attendance(           # Student attendance is created and stored
        roll_number=data['roll_number'],
        date=data['date'],
        status=data['status']
    )
    attendance_date = data.get('date', str(date.today()))

    existing = Attendance.query.filter_by(roll_number=data['roll_number'], date=attendance_date).first()
    if existing:
        return jsonify({"error": "Attendance already marked for this student on this date"}), 400
     #  It prevents marking the same student twice on the same day

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
