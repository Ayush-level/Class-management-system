from flask import request,jsonify,Blueprint
from datetime import date

Students = [
    {
        'id': 1,
        'name': 'Rahul Sharma',
        'roll_number': '001',
        'class': '10',
        'section': 'A',
        'gender': 'Male',
        'dob': '2010-05-15',
        'category': 'General',
        'father_name': 'Vijay Sharma',
        'mother_name': 'Priya Sharma',
        'address': '123 Main Street, Mumbai',
        'contact': '9876543210',
        'admission_number': 'ADM2023001',
        'admission_date': '2023-04-01',
        'aadhaar': '1234-5678-9012',
        'religion': 'Hindu',
        'blood_group': 'O+',
        'previous_school': 'ABC School'
    },
    {
        'id': 2,
        'name': 'Priya Patel',
        'roll_number': '002',
        'class': '10',
        'section': 'A',
        'gender': 'Female',
        'dob': '2010-08-22',
        'category': 'OBC',
        'father_name': 'Rajesh Patel',
        'mother_name': 'Anjali Patel',
        'address': '456 Park Avenue, Mumbai',
        'contact': '9876543211',
        'admission_number': 'ADM2023002',
        'admission_date': '2023-04-01',
        'aadhaar': '2234-5678-9012',
        'religion': 'Hindu',
        'blood_group': 'A+',
        'previous_school': 'XYZ School'
    }
]


next_student_id = 3

student_bp = Blueprint("dashboard", __name__)

@student_bp.route("/students", methods=["GET"])
def dashboard():

    students = Student.query.all()

    data = []

    for s in students:
        data.append({
            "id": s.id,
            "name": s.name,
            "gender": s.gender,
            "gp_url": f"/students/{s.id}",
            "ep_url": f"/students/{s.id}/enrollment"
        })

    return jsonify(data)





 # All URLs in this file start with `/api/students`



@student_bp.route("/add_student", methods=["POST"]) 
def Student_details():
    data=request.get_json() 
    required_fields=['name','date_of_birth','gender','father_name','mother_name','date_of_admission' ,'phone_no','address','email','blood_group']
    # A list of required fields





    for field in required_fields:
       if field not in data:# Check if NOT all fields are present
           return jsonify({"error":f"Missing {field}"}),400
    
    create_student = student(
       
        name=data['name'],
        date_of_birth=data['date_of_birth'],
        gender=data['gender'],
        father_name=data['father_name'],
        mother_name=data['mother_name'],
        date_of_admission=data['date_of_admission'],
        phone_no=data['phone_no'],
        address=data['address'],
        email=data['email'],
        blood_group=data['blood_group']
    )
    db.session.add(create_student) # Add student to database session
    db.session.commit()
    return jsonify({"message":"Student added successfully"}),201





@student_bp.route("/<int:student_rlno>", methods=["GET"]) 
def get_student(student_rlno):
    students = student.query.get(student_rlno)

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
        "blood_group":student.blood_group
    }),200
    

