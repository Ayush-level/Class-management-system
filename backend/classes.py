from flask import Blueprint, jsonify
from models.school_class import SchoolClass
from models.db import db

class_bp = Blueprint("classes", __name__)

@class_bp.route("/classes", methods=["GET"])
def get_classes():
    classes = SchoolClass.query.all()
    return jsonify([c.to_dict() for c in classes])