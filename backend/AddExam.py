from flask import request,jsonify,Blueprint
from datetime import date
from models.school_class import SchoolClass
from models.db import db
from models.exam import Exam
from models.exam_mark import ExamMark



exam_bp = Blueprint("exam", __name__)

@exam_bp.route("/classes/<int:class_id>/exam", methods=["POST"])   
def add_exam(class_id):

    school_class = SchoolClass.query.filter_by(id=class_id).first()
    if not school_class:
        return jsonify({"error":"Class not found"}),404
    data = request.get_json()

    required_fields = ['exam_name','test_id','subject_1','subject_2','subject_3','subject_4','subject_5','subject_6','subject_1maxmarks','subject_2maxmarks','subject_3maxmarks','subject_4maxmarks','subject_5maxmarks','subject_6maxmarks']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error":f"Missing {field}"}),400
    
    create_exam = Exam(
        class_id=class_id,
        exam_name = data['exam_name'],
        test_id=data['test_id'],
        subject_1=data['subject_1'],
        subject_2=data['subject_2'],
        subject_3=data['subject_3'],
        subject_4=data['subject_4'],
        subject_5=data['subject_5'],
        subject_6=data['subject_6'],
        subject_1maxmarks=data['subject_1maxmarks'],
        subject_2maxmarks=data['subject_2maxmarks'],
        subject_3maxmarks=data['subject_3maxmarks'],
        subject_4maxmarks=data['subject_4maxmarks'],
        subject_5maxmarks=data['subject_5maxmarks'],
    subject_6maxmarks=data['subject_6maxmarks']
)
    db.session.add(create_exam)
    db.session.commit()
    return jsonify({"message":"Exam added successfully"}),201


@exam_bp.route("/classes/<int:class_id>/<int:test_id>", methods=["GET"])
def get_exam(class_id,test_id):
    exam = Exam.query.filter_by(class_id=class_id,test_id=test_id).first()
    if not exam:
        return jsonify({"error":"Exam not found"}),404
    
    return jsonify({
   "class_id": exam.class_id,
   "exam_name": exam.exam_name,
   "test_id": exam.test_id,
   "subject_1": exam.subject_1,
   "subject_2": exam.subject_2,
   "subject_3": exam.subject_3,
   "subject_4": exam.subject_4,
   "subject_5": exam.subject_5,
   "subject_6": exam.subject_6,
   "subject_1maxmarks": exam.subject_1maxmarks,
   "subject_2maxmarks": exam.subject_2maxmarks,
   "subject_3maxmarks": exam.subject_3maxmarks,
   "subject_4maxmarks": exam.subject_4maxmarks,
   "subject_5maxmarks": exam.subject_5maxmarks,
   "subject_6maxmarks": exam.subject_6maxmarks
}),200



exam_mark = Blueprint("exam_mark", __name__)

@exam_mark.route("/classes/<int:class_id>/<int:test_id>/<int:roll_number>/exam_mark", methods=["POST"])
def add_exam_mark(class_id,test_id,roll_number):
    exam = Exam.query.filter_by(class_id=class_id,test_id=test_id).first()
    if not exam:
        return jsonify({"error":"Exam not found"}),404
    data = request.get_json()
    required_fields = ['subject_1marks','subject_2marks','subject_3marks','subject_4marks','subject_5marks','subject_6marks']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error":f"Missing {field}"}),400
    
    create_markstable = ExamMark(
         class_id=class_id,
        test_id=test_id, 
        roll_number=roll_number,
        subject_1marks=data['subject_1marks'],
        subject_2marks=data['subject_2marks'],
        subject_3marks=data['subject_3marks'],
        subject_4marks=data['subject_4marks'],
        subject_5marks=data['subject_5marks'],
        subject_6marks=data['subject_6marks']
)
    db.session.add(create_markstable)
    db.session.commit()
    return jsonify({"message":"Exam mark added successfully"}),201
    
   
@exam_mark.route("/classes/<int:class_id>/<int:test_id>/<int:roll_number>/exam_mark", methods=["GET"])

def get_marks(class_id,test_id,roll_number):
    
    mark = ExamMark.query.filter_by(class_id=class_id,test_id=test_id,roll_number=roll_number).first()
    if not mark:
        return jsonify({"error":"Mark not found"}),404
    
    return jsonify({
        "class_id":mark.class_id,
        "test_id":mark.test_id, 
        "roll_number":mark.roll_number,
       "subject_1marks":mark.subject_1marks,
       "subject_2marks":mark.subject_2marks,
       "subject_3marks":mark.subject_3marks,
       "subject_4marks":mark.subject_4marks,
       "subject_5marks":mark.subject_5marks,
       "subject_6marks":mark.subject_6marks
    }),200