from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    title = db.Column(db.String(80), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Todo('{self.title}', due '{self.due_date}', status '{self.status}')"

@app.route('/')
def index():
    return render_template("index.html")
# @app.route('/about')
# def about():
#     return "I am Mayank Bansal"
# @app.route('/contact')
# def contact():
#     return "My email is- bansalmayank1414@gmail.com"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)