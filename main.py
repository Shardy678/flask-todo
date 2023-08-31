from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy()
db.init_app(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content')
    new_task = Task(content=content)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get(id)
    task.completed = True
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')


sample_tasks_created = False

@app.before_request
def create_sample_tasks():
    global sample_tasks_created
    if not sample_tasks_created:
        with app.app_context():
            db.create_all()
            sample_tasks = [
                Task(content='Buy groceries'),
                Task(content='Finish work project'),
                Task(content='Go for a run')
            ]
            db.session.bulk_save_objects(sample_tasks)
            db.session.commit()
            sample_tasks_created = True

if __name__ == '__main__':
    app.run(debug=True)
