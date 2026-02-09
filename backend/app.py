from flask import Flask
from extensions import db

from Dashboard import student_bp
from attendence import attendance_bp
from classes import class_bp
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)        

@app.route("/")
def ping():
    return {"message": "pong"}

app.register_blueprint(student_bp,url_prefix="/api/student")
app.register_blueprint(attendance_bp,url_prefix="/api/attendance")
app.register_blueprint(class_bp,url_prefix="/api/class")





if __name__ =='__main__':
   with app.app_context():
        db.create_all()
        print("Data created successfully")
   app.run(debug=True)
