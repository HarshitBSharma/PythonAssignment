from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
db = SQLAlchemy(app)


class Student(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    classID = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.utcnow())
    children = db.relationship('ClassTable', backref='student', lazy=True)


class ClassTable(db.Model):
    Class_ID = db.Column(db.Integer, db.ForeignKey('student.classID'), primary_key=True)
    Class_name = db.Column(db.String(10))
    Class_Leader = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.utcnow())


def pre_populate():
    classID1 = 1
    class1Name = 'Extc'
    classID2 = 2
    class2Name = 'CMPN'
    class1 = ClassTable(Class_ID=classID1, Class_name=class1Name)
    class2 = ClassTable(Class_ID=classID2, Class_name=class2Name)
    try:
        db.session.add(class1)
        db.session.add(class2)
    except Exception as e:
        return e


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        students = Student.query.order_by(Student.created_on).all()
        classes = ClassTable.query.order_by(ClassTable.created_on).all()
        return render_template('index.html', students=students, classes=classes)


@app.route("/new_student", methods=['POST', 'GET'])
def add_new_student():
    if request.method == 'POST':
        student_name = request.form['studentName']
        student_class = request.form['className']
        new_student = Student(classID=2, name=student_name)
        new_class = ClassTable(Class_ID=1, Class_name=student_class)
        try:
            db.session.add(new_student)
            db.session.commit()
            return "data added successfully"
        except Exception as e:
            return "There was an issue adding your data {}".format(str(e))
    else:
        return render_template("NewStudent.html")


if __name__ == "__main__":
    pre_populate()
    app.run(debug=True)
