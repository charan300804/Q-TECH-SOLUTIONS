from flask import Flask, render_template, request, redirect, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

FILENAME = "tasks.json"

def load_tasks():
    if os.path.exists(FILENAME) and os.path.getsize(FILENAME) > 0:
        with open(FILENAME, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # Return an empty list if JSON is invalid
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    tasks = load_tasks()
    description = request.form.get("description")
    due_date = request.form.get("due_date") or None
    priority = request.form.get("priority", "Medium")

    task = {
        "description": description,
        "due_date": due_date,
        "priority": priority,
        "completed": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:index>", methods=["POST"])
def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        del tasks[index]
        save_tasks(tasks)
    return redirect("/")

@app.route("/complete/<int:index>", methods=["POST"])
def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        save_tasks(tasks)
    return redirect("/")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

if __name__ == "__main__":
    app.run(debug=True)
