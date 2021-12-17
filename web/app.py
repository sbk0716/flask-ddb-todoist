from flask import Flask, render_template, request, redirect
import requests
import os
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, HiddenField, SelectField

app = Flask(__name__)

# Enable CSRF measures
app.config["SECRET_KEY"] = "123456789"
app.config["WTF_CSRF_ENABLED"] = True

# Define API url
backend_url = os.getenv("BACKEND_URL", "http://localhost:5000")
task_url = f"""{backend_url}/tasks"""

class TaskForm(FlaskForm):
    """
    Taskform Class
    This class inherits from FlaskForm.
    """
    # For CSRF measures
    hidden_field_1 = HiddenField("HiddenField 1")
    hidden_field_2 = HiddenField("HiddenField 2")
    hidden_field_3 = HiddenField("HiddenField 3")
    hidden_field_4 = HiddenField("HiddenField 4")
    # Set task form to add task
    task = StringField(validators=[DataRequired()])
    detail = StringField(validators=[DataRequired()])
    status = SelectField(validators=[DataRequired()], choices=[("TODO"), ("WIP"), ("DONE")])
    submit = SubmitField("Resister")

# Display top page
@app.route("/", methods=["GET"])
def index():
    """
    Execute requests.get
    https://qiita.com/sqrtxx/items/49beaa3795925e7de666
    """
    r = requests.get(task_url)
    r.raise_for_status()
    tasks = r.json()
    return render_template("index.html", tasks=tasks)

@app.route("/create-task", methods=["GET", "POST"])
def create():
    form = TaskForm()
    # Display create page
    if request.method == "GET":
        return render_template("create.html", form=form)
    else:
        """
        Execute form.validate_on_submit()
        https://flask-wtf.readthedocs.io/en/0.15.x/quickstart/
        """
        if form.validate_on_submit():
            task = request.form.get("task")
            detail = request.form.get("detail")
            status = request.form.get("status")
            payload = {
                "task":task,
                "detail":detail,
                "status":status
            }
            r = requests.post(task_url, json=payload)
            r.raise_for_status()
            return redirect("/")
        # In case of error
        else:
            return render_template("create.html", form=form)

@app.route("/detail/<taskId>", methods=["GET"])
def detail(taskId):
    taskId_url = f"""{task_url}/{taskId}"""
    r = requests.get(taskId_url)
    r.raise_for_status()
    tasks = r.json()
    return render_template("detail.html", tasks=tasks)

@app.route("/delete/<taskId>", methods=["GET"])
def delete(taskId):
    taskId_url = f"""{task_url}/{taskId}"""
    requests.delete(taskId_url)
    return redirect("/")

@app.route("/update/<taskId>", methods=["GET", "POST"])
def update(taskId):
    form = TaskForm()
    taskId_url = f"""{task_url}/{taskId}"""
    r = requests.get(taskId_url)
    r.raise_for_status()
    tasks = r.json()
    if request.method == "GET":
        return render_template("update.html", tasks=tasks, form=form)
    else:
        if form.validate_on_submit():
            print("recieve task")
            task = request.form.get("task")
            detail = request.form.get("detail")
            status = request.form.get("status")
            payload = {
                "task":task,
                "detail":detail,
                "status":status
            }
            requests.put(taskId_url, json=payload)
            return redirect("/")
        else:
            return render_template("update.html", tasks=tasks, form=form)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)