from flask import Flask
from model import db
from route import student_ID

app = Flask(__name__)




db.init_app(app)
app.register_blueprint(student_ID)



@app.route("/")
def crete_data():
    db.create_all()
    return "Data created successfully"


if __name__ =='__main__':
   app.run(debug=True)
