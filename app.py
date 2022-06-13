from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)  # Initialise app

# config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
db = SQLAlchemy(app)


# Database Table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(200))
    email = db.Column(db.String(200))
    contact = db.Column(db.Integer)
    course = db.Column(db.String(200))

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students = students)


@app.route('/add', methods = ['GET', 'POST'])
def add():
        if request.method == 'POST':
               name = request.form['name']
               email = request.form['email']
               contact = request.form['contact']
               course = request.form['course']
               new_student = Student(name = name, email = email, contact = contact, course = course)
               db.session.add(new_student)
               db.session.commit() 
               return redirect('/')

        else:
              return render_template('add.html')

 
@app.route('/edit/<int:id>',methods = ['GET','POST'])
def update(id):
    student = Student.query.filter_by(id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            name = request.form['name']
            email = request.form['email']
            contact = request.form['contact']
            course = request.form['course']
            student = Student(name = name, email = email, contact = contact, course = course)
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        return f"Student with id = {id} Does nit exist"
 
    return render_template('edit.html', student = student)

# Delete Route
@app.route('/delete/<int:id>')
def deleteStudent(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
