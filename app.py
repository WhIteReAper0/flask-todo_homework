from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from extensions import db 
from models import Task

app = Flask(__name__)

app.config['SECRET_KEY'] = '22022022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add():
    title = request.form.get('title')
    if title:
        new_task = Task(title=title.strip())
        db.session.add(new_task)
        db.session.commit()
        flash('Task add!', 'success')
        
    return render_template('add.html')
    


@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task =Task.query.get_or_404(id)
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.compete = 'complete' in request.form 
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('task deleted', 'danger')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
