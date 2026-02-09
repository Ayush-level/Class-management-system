
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
