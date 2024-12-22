from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Task model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    title = db.Column(db.String(80), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Todo('{self.title}', created '{self.created}', due '{self.due_date}', status '{self.status}')"

# Route for displaying and adding tasks
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        title = request.form['title']
        due_date = request.form['due_date']

        # Validate form data
        if not title or not due_date:
            return "Title and Due Date are required!", 400

        # Convert due_date string to a datetime.date object
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD.", 400

        # Add task to the database
        new_task = Todo(title=title, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index'))  # Redirect to the home page

    # Query all tasks (displaying them on the page)
    tasks = Todo.query.order_by(Todo.status.desc(), Todo.due_date).all()
    return render_template("index.html", tasks=tasks)

# Endpoint for updating task status via AJAX
@app.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    task = Todo.query.get_or_404(task_id)

    # Toggle status between "Pending" and "Completed"
    if task.status == "Pending":
        task.status = "Completed"
    else:
        task.status = "Pending"

    db.session.commit()

    return jsonify({"status": task.status})

@app.route('/Delete/<int:task_id>')
def delete(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
