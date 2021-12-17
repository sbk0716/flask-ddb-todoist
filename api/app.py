from flask import Flask, request
from usecases import task

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route("/")
def health():
    return "I'm alive!"

@app.route("/tasks", methods=["POST"])
def create_task():
    print("### execute create_task method")
    body = request.get_json()
    print("PRINT: body")
    print("body")
    return task.create(body)

@app.route("/tasks", methods=["GET"])
def get_all_task():
    print("### execute get_all_task method")
    return task.get_all()

@app.route("/tasks/<taskId>", methods=["GET"])
def get_task(taskId):
    print("### execute get_task method")
    return task.get(taskId)

@app.route("/tasks/<taskId>", methods=["DELETE"])
def delete_task(taskId):
    print("### execute delete_task method")
    return task.delete(taskId)

@app.route("/tasks/<taskId>", methods=["PUT"])
def update_task(taskId):
    print("### execute put_task method")
    body = request.get_json()
    print("PRINT: body")
    print("body")
    return task.update(taskId, body)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
