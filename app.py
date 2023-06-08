from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

# Define your Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20))

    def toggle_status(self):
        if self.status == "Complete":
            self.status = "Incomplete"
        elif self.status == "Incomplete":
            self.status = "Complete"

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    per_page = 2  # Number of tasks per page
    page = int(request.args.get('page', 1))  # Get the current page from the query parameter

    if request.method == 'POST':
        # Create a new task
        title = request.form['title']
        description = request.form['description']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        status = request.form['status']

        new_task = Task(title=title, description=description, due_date=due_date, status=status)
        db.session.add(new_task)
        db.session.commit()

        return redirect('/tasks')

    else:
        # Retrieve paginated tasks
        tasks = Task.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # Find the task with the given ID
    task = Task.query.get(task_id)

    if task:
        # Delete the task from the database
        db.session.delete(task)
        db.session.commit()

    return redirect('/tasks')

@app.route('/tasks/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.toggle_status()
        db.session.commit()

    return redirect('/tasks')
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Find the task with the given ID
    task = Task.query.get(task_id)

    if task:
        return render_template('get.html', tasks=tasks)
    else:
        return "Task not found"
if __name__ == '__main__':
    app.run()
