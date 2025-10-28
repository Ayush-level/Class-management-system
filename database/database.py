import mysql.connector as Mysql 
import pandas as pd

credentials = {
    "host": "localhost",
    "user": "root",
    "password": "mysql",
    "database": "class"
}
# Connect to the MySQL database

try:
    mysql = Mysql.connect(**credentials)
    cursor = mysql.cursor()
except Mysql.errors.ProgrammingError as e:
    host = credentials["host"]
    user = credentials["user"]
    password = credentials["password"]
    database = credentials["database"]
    mysql = Mysql.connect(host=host, user=user, password=password)
    cursor = mysql.cursor()
    cursor.execute(f"CREATE DATABASE {database}")
    cursor.execute(f"USE {database}")
    cursor.execute("""CREATE TABLE students (Rollno INT AUTO_INCREMENT PRIMARY KEY,
     Name VARCHAR(255),
      Father_Name VARCHAR(255),
       Mother_Name VARCHAR(255),
        DOB DATE,
         Gender CHAR(1) CHECK (Gender IN ('M', 'F')),
         Number BIGINT,
         Status CHAR(1) CHECK (Status IN ('P', 'A', 'L')),
         DOA DATE)""")
    cursor.execute("""CREATE TABLE Attendance (Rollno INT, Date DATE,
     Status CHAR(1) CHECK (Status IN ('P', 'A', 'L')))""")
    cursor.execute("""CREATE TABLE Test_Table (TEST VARCHAR(255),
     Subject1 VARCHAR(255),
      Subject2 VARCHAR(255),
       Subject3 VARCHAR(255),
        Subject4 VARCHAR(255),
         Subject5 VARCHAR(255),
          Subject6 VARCHAR(255),
           Subject1_mark INT,
            Subject2_mark INT,
             Subject3_mark INT,
              Subject4_mark INT,
               Subject5_mark INT,
                Subject6_mark INT)""")
    mysql.commit()
    cursor.close()
    mysql.close()
    mysql = Mysql.connect(**credentials)
    cursor = mysql.cursor()
except Mysql.errors.DatabaseError as e:
    print("Turn on the MySQL server")
    print(e)
except Exception as e:
    print("Error connecting to MySQL:", e)
    print(type(e))

def mainTable():
    sql = "SELECT * FROM students"
    cursor.execute(sql)
    result = pd.DataFrame(cursor.fetchall(), columns=[i[0] for i in cursor.description])
    return result

def addStudent(Name,Father_Name,Mother_Name,DOB,Gender,Number,Status,DOA):
    try:
        sql = "INSERT INTO students (Name,Father_Name,Mother_Name,DOB,Gender,Number,Status,DOA) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(Name,Father_Name,Mother_Name,DOB,Gender,Number,Status,DOA))
        mysql.commit()
    except Exception as e:
        return e
    return True

def test(Name,Subject1,Subject2,Subject3,Subject4,Subject5,Subject6,Subject1_mark,Subject2_mark,Subject3_mark,Subject4_mark,Subject5_mark,Subject6_mark):
    try:
        sql = "INSERT INTO Test_Table (Name,Subject1,Subject2,Subject3,Subject4,Subject5,Subject6,Subject1_mark,Subject2_mark,Subject3_mark,Subject4_mark,Subject5_mark,Subject6_mark) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(Name,Subject1,Subject2,Subject3,Subject4,Subject5,Subject6,Subject1_mark,Subject2_mark,Subject3_mark,Subject4_mark,Subject5_mark,Subject6_mark))
        mysql.commit()
        sql = f"""CREATE TABLE IF NOT EXIST {Name} 
        (Rollno INT FOREIGN KEY (Rollno) REFERENCES students(Rollno)PRIMARY KEY,
         {Subject1} INT DEFAULT 0 CHECK ({Subject1} BETWEEN 0 AND {Subject1_mark}),
          {Subject2} INT DEFAULT 0 CHECK ({Subject2} BETWEEN 0 AND {Subject2_mark}),
           {Subject3} INT DEFAULT 0 CHECK ({Subject3} BETWEEN 0 AND {Subject3_mark}),
            {Subject4} INT DEFAULT 0 CHECK ({Subject4} BETWEEN 0 AND {Subject4_mark}),
             {Subject5} INT DEFAULT 0 CHECK ({Subject5} BETWEEN 0 AND {Subject5_mark}),
              {Subject6} INT DEFAULT 0 CHECK ({Subject6} BETWEEN 0 AND {Subject6_mark}))"""
        mysql.commit()
    except Exception as e:
        return e
    return True