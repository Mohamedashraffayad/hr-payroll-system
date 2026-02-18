
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
import bcrypt

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "CHANGE_THIS_SECRET_KEY"
jwt = JWTManager(app)

# In-memory database (replace with real DB in production)
users = [
    {
        "id": 1,
        "username": "admin",
        "password": bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()),
        "role": "admin"
    },
    {
        "id": 2,
        "username": "employee1",
        "password": bcrypt.hashpw("emp123".encode(), bcrypt.gensalt()),
        "role": "employee"
    }
]

leave_requests = []


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username and bcrypt.checkpw(password.encode(), user["password"]):
            token = create_access_token(identity={
                "id": user["id"],
                "role": user["role"]
            })
            return jsonify(access_token=token)

    return jsonify(msg="Invalid credentials"), 401


@app.route("/leave/request", methods=["POST"])
@jwt_required()
def request_leave():
    user = get_jwt_identity()

    if user["role"] != "employee":
        return jsonify(msg="Only employees can request leave"), 403

    data = request.json
    leave = {
        "id": len(leave_requests) + 1,
        "employee_id": user["id"],
        "start_date": data["start_date"],
        "end_date": data["end_date"],
        "reason": data["reason"],
        "status": "pending"
    }
    leave_requests.append(leave)
    return jsonify(msg="Leave request submitted")


@app.route("/leave/all", methods=["GET"])
@jwt_required()
def get_all_leaves():
    user = get_jwt_identity()

    if user["role"] != "admin":
        return jsonify(msg="Admin only"), 403

    return jsonify(leave_requests)


@app.route("/leave/update/<int:leave_id>", methods=["PUT"])
@jwt_required()
def update_leave(leave_id):
    user = get_jwt_identity()

    if user["role"] != "admin":
        return jsonify(msg="Admin only"), 403

    data = request.json
    status = data.get("status")

    for leave in leave_requests:
        if leave["id"] == leave_id:
            leave["status"] = status
            return jsonify(msg="Updated successfully")

    return jsonify(msg="Not found"), 404


if __name__ == "__main__":
    app.run(debug=True)
