from flask import  request,jsonify,Blueprint
from model import db, Attendance ,student,exam,marks,subject # model is file which Raj will make define what a Student looks like in the database
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

attendance_percentage_bp = Blueprint("attendance_percentage", __name__, url_prefix='/api/attendance_percentage') 

@attendance_percentage_bp.route('/api/attendance_percentage/', methods = ['GET'])
def attendance_percentage():
    min_attendance = request.args.get('min_attendance', default=75, type=float)
    students = student.query.all()
    
    below_min = []
    
    for student in students:
        total_days = Attendance.query.filter_by(roll_number=student.roll_number).count()
        present_days = Attendance.query.filter_by(roll_number=student.roll_number, status='Present').count()
        
        if total_days==0:
            percentage = 0
        else:
            percentage = (present_days/total_days)*100
        
        if percentage < min_attendance:
            below_min.append(student)
    
    return jsonify({
        "students": [student.to_dict() for student in below_min], "percentage": percentage
        })


exam_bp = Blueprint('exam', __name__, url_prefix='/api/exam')

@exam_bp.route('/api/exam/add', methods=['POST'])
def add_exam():
    data = request.get_json()
    name = data.get('name')
    date = data.get('date')
    
    new_exam = exam(name = name,date = date)
    db.session.add(new_exam)
    db.session.commit()
    return jsonify({"message":"Exam added successfully"}),201


@exam_bp.route('api/subjects/add', methods=['POST'])
def add_subject():
    data = request.get_json()
    name = data.get('name')

    if subject.query.filter_by(name=name).first():
        return jsonify({"error":"Subject already exists"}),400
    
    new_subject = subject(name = name)
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({"message":"Subject added successfully"}),201


@exam_bp.route('api/marks/add', methods=['POST'])
def add_marks():
    data = request.get_json()
    student_name = data.get('student_name')
    roll_number = data.get('roll_number')
    subject_name = data.get('subject_name')
    theroy_marks = data.get('theroy_marks')
    internal_marks = data.get('internal_marks')

    if marks.query.filter_by(roll_number=roll_number, subject_name=subject_name).first():
        return jsonify({"error":"Marks already exists"}),400

    if theroy_marks > 80 or internal_marks > 20:
        return jsonify({"error":"Invalid marks"}),400

    total_marks = theroy_marks + internal_marks
    
    new_marks = marks(roll_number=roll_number,  subject_name=subject_name, theroy_marks=theroy_marks, internal_marks=internal_marks, total_marks=total_marks)
    db.session.add(new_marks)
    db.session.commit()
    return jsonify({"message":"Marks added successfully"}),201


if __name__ == "__main__":
    app.run(debug=True)