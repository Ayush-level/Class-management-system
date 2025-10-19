from flask import  request,jsonify,Blueprint
from model import db, student


student_ID = Blueprint("student", __name__, url_prefix='/api/student')

@student_ID.route('/api/student', methods=["POST"])
def Student_details():
    data=request.get_json()
    required_fields=['name','date_of_birth','gender','father_name','mother_name','date_of_admission' ,'phone_no','address','email']
    
    for field in required_fields:
     if not data.get(field):
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
        email=data['email']
    )
    db.session.add(create_student)
    db.session.commit()
    return jsonify({"message":"Student added successfully"}),201

if __name__ == "__main__":
    app.run(debug=True)
