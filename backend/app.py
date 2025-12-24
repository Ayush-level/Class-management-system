from flask import Flask

from route import student_ID

app = Flask(__name__)

@app.route("/")
def ping():
    return {"message": "pong"}
app.register_blueprint(student_ID,url_prefix="/api/student_id")





if __name__ =='__main__':
   with app.app_context():
        db.create_all()
        print("Data created successfully")
   app.run(debug=True)
