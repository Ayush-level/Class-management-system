from sqlalchemy import create_engine, Integer, MetaData, Table, Column, String, Date, CheckConstraint, ForeignKey
import pandas as pd

credentials = {
    "host": "localhost",
    "user": "root",
    "password": "mysql",
    "database": "class",
    "port" : 3306
}

engine = create_engine(f"mysql+mysqlconnector://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['database']}") 

metadata = MetaData()
mainTable = Table("main",
            metadata,
            Column("Roll",Integer,primary_key=True, autoincrement=True),
            Column("Name", String(255)),
            Column("Father_Name", String(255)),
            Column("Mother_Name", String(255)),
            Column("DOB", Date),
            Column("Gender", String(1), CheckConstraint("Gender IN ('M', 'F')")),
            Column("Status", String(1), CheckConstraint("Status IN ('P', 'A', 'L')")),
            Column("DOA", Date)
            )

attendanceTable = Table("attendance",
            metadata,
            Column("Roll",Integer),
            Column("Date", Date),
            Column("Status", String(1), CheckConstraint("Status IN ('P', 'A', 'L')"))
            )

testTable = Table("test",
            metadata,
            Column("test",String(255)),
            Column("Subject1", String(255)),
            Column("Subject2", String(255)),
            Column("Subject3", String(255)),            
            Column("Subject4", String(255)),            
            Column("Subject5", String(255)),            
            Column("Subject6", String(255)),            
            Column("Subject1_mark", Integer),            
            Column("Subject2_mark", Integer),            
            Column("Subject3_mark", Integer),            
            Column("Subject4_mark", Integer),            
            Column("Subject5_mark", Integer),            
            Column("Subject6_mark", Integer)
            )

def createTest(name):
    return Table(name,
            metadata,
            Column("Roll",Integer, ForeignKey("main.Roll")),
            Column("Subject1", Integer, CheckConstraint("Subject1 BETWEEN 0 AND Subject1_mark"), default=0,),
            Column("Subject2", Integer, CheckConstraint("Subject2 BETWEEN 0 AND Subject2_mark"), default=0,),
            Column("Subject3", Integer, CheckConstraint("Subject3 BETWEEN 0 AND Subject3_mark"), default=0,),
            Column("Subject4", Integer, CheckConstraint("Subject4 BETWEEN 0 AND Subject4_mark"), default=0,),
            Column("Subject5", Integer, CheckConstraint("Subject5 BETWEEN 0 AND Subject5_mark"), default=0,),
            Column("Subject6", Integer, CheckConstraint("Subject6 BETWEEN 0 AND Subject6_mark"), default=0,)
            )

def addStudent(Name,Father_Name,Mother_Name,DOB,Gender,Number,Status,DOA):
    return mainTable.insert().values(Name=Name,Father_Name=Father_Name,Mother_Name=Mother_Name,DOB=DOB,Gender=Gender,Number=Number,Status=Status,DOA=DOA)

metadata.create_all(engine)
metadata.reflect(bind=engine)