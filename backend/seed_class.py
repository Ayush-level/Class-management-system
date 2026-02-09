from app import create_app
from extensions import db
from models.school_class import SchoolClass

app = create_app()

def seed_classes():

    with app.app_context():

        class_names = ["1", "2", "3", "4", "5"]

        for name in class_names:

            exists = SchoolClass.query.filter_by(name=name).first()

            if not exists:
                db.session.add(SchoolClass(name=name))

        db.session.commit()

        print("✅ Classes created successfully")



