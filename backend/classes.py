from flask import Blueprint, jsonify
from services import class_service
from exceptions import ServiceException, NotFoundException

class_bp = Blueprint("classes", __name__)

@class_bp.route("/classes", methods=["GET"])
def get_classes():
    try:
        classes = class_service.get_all_classes()
        return jsonify([c.to_dict() for c in classes])
    except ServiceException as e:
        return jsonify({"error": e.message, "error_code": e.error_code}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500