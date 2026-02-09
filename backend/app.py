from flask import Flask

from Dashboard import student_bp

app = Flask(__name__)

@app.route("/")
def ping():
    return {"message": "pong"}

app.register_blueprint(student_bp,url_prefix="/api/student")





if __name__ =='__main__':
   with app.app_context():
        db.create_all()
        print("Data created successfully")
   app.run(debug=True)
