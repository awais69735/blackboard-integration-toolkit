"""Flask-based mock Blackboard REST API server."""

import json
from flask import Flask, request, jsonify
import os
import uuid
from typing import Dict, Any, List

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def load_fixture(filename: str) -> Any:
    with open(os.path.join(FIXTURES_DIR, filename), "r") as f:
        return json.load(f)


def create_app():
    app = Flask(__name__)

    # Load fresh data per app instance
    users_data = load_fixture("users.json")["results"]
    courses_data = load_fixture("courses.json")["results"]
    enrollments_data = load_fixture("enrollments.json")
    assignments_data = load_fixture("assignments.json")

    def _paginate(items: List[Dict], limit: int, offset: int) -> tuple[List[Dict], int]:
        total = len(items)
        paginated = items[offset:offset + limit]
        return paginated, total

    # ---------- TOKEN ENDPOINT (for OAuth2) ----------
    @app.route("/learn/api/public/v1/oauth2/token", methods=["POST"])
    def token():
        """Return a dummy OAuth2 token."""
        return jsonify({
            "access_token": "mock_access_token",
            "token_type": "Bearer",
            "expires_in": 3600
        })

    # ---------- USERS (v1) ----------
    @app.route("/learn/api/public/v1/users", methods=["GET"])
    def get_users():
        username = request.args.get("userName")
        if username:
            filtered = [u for u in users_data if u["userName"] == username]
        else:
            filtered = users_data
        active = request.args.get("active")
        if active is not None:
            active_bool = active.lower() == "true"
            filtered = [u for u in filtered if u["active"] == active_bool]
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        paginated, total = _paginate(filtered, limit, offset)
        return jsonify({"results": paginated, "totalCount": total})

    @app.route("/learn/api/public/v1/users/<user_id>", methods=["GET"])
    def get_user(user_id):
        user = next((u for u in users_data if u["id"] == user_id), None)
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user)

    @app.route("/learn/api/public/v1/users/<user_id>", methods=["PATCH"])
    def patch_user(user_id):
        user = next((u for u in users_data if u["id"] == user_id), None)
        if not user:
            return jsonify({"message": "User not found"}), 404
        data = request.json
        for key in ["userName", "email", "firstName", "lastName", "active"]:
            if key in data:
                user[key] = data[key]
        return jsonify(user)

    @app.route("/learn/api/public/v1/users", methods=["POST"])
    def create_user():
        data = request.json
        if "userName" not in data:
            return jsonify({"message": "Missing userName"}), 400
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "userName": data["userName"],
            "email": data.get("email"),
            "firstName": data.get("firstName"),
            "lastName": data.get("lastName"),
            "active": data.get("active", True),
            "created": "2023-01-01T00:00:00Z",
            "modified": "2023-01-01T00:00:00Z"
        }
        users_data.append(user)
        return jsonify(user), 201

    @app.route("/learn/api/public/v1/users/<user_id>", methods=["DELETE"])
    def delete_user(user_id):
        user = next((u for u in users_data if u["id"] == user_id), None)
        if not user:
            return jsonify({"message": "User not found"}), 404
        users_data[:] = [u for u in users_data if u["id"] != user_id]
        return "", 204

    # ---------- COURSES (v3) ----------
    @app.route("/learn/api/public/v3/courses", methods=["GET"])
    def get_courses_v3():
        course_id = request.args.get("courseId")
        if course_id:
            filtered = [c for c in courses_data if c["courseId"] == course_id]
        else:
            filtered = courses_data
        user_id = request.args.get("userId")
        if user_id:
            enrolled_course_ids = []
            for cid, enrollments in enrollments_data.items():
                for e in enrollments:
                    if e["userId"] == user_id:
                        enrolled_course_ids.append(cid)
                        break
            filtered = [c for c in filtered if c["id"] in enrolled_course_ids]
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        paginated, total = _paginate(filtered, limit, offset)
        return jsonify({"results": paginated, "totalCount": total})

    @app.route("/learn/api/public/v3/courses/<course_id>", methods=["GET"])
    def get_course_v3(course_id):
        course = next((c for c in courses_data if c["id"] == course_id), None)
        if not course:
            return jsonify({"message": "Course not found"}), 404
        return jsonify(course)

    @app.route("/learn/api/public/v3/courses/<course_id>", methods=["PATCH"])
    def patch_course_v3(course_id):
        course = next((c for c in courses_data if c["id"] == course_id), None)
        if not course:
            return jsonify({"message": "Course not found"}), 404
        data = request.json
        for key in ["name", "courseId", "description", "available"]:
            if key in data:
                course[key] = data[key]
        return jsonify(course)

    @app.route("/learn/api/public/v3/courses", methods=["POST"])
    def create_course_v3():
        data = request.json
        if "name" not in data or "courseId" not in data:
            return jsonify({"message": "Missing name or courseId"}), 400
        course_id = str(uuid.uuid4())
        course = {
            "id": course_id,
            "name": data["name"],
            "courseId": data["courseId"],
            "description": data.get("description"),
            "available": data.get("available", True),
            "created": "2023-01-01T00:00:00Z",
            "modified": "2023-01-01T00:00:00Z"
        }
        courses_data.append(course)
        return jsonify(course), 201

    @app.route("/learn/api/public/v3/courses/<course_id>", methods=["DELETE"])
    def delete_course_v3(course_id):
        course = next((c for c in courses_data if c["id"] == course_id), None)
        if not course:
            return jsonify({"message": "Course not found"}), 404
        courses_data[:] = [c for c in courses_data if c["id"] != course_id]
        return "", 204

    # ---------- ENROLLMENTS (v1) ----------
    @app.route("/learn/api/public/v1/courses/<course_id>/enrollments", methods=["GET"])
    def get_enrollments(course_id):
        if course_id not in enrollments_data:
            return jsonify({"results": [], "totalCount": 0})
        enrollments = enrollments_data[course_id]
        active = request.args.get("active")
        if active is not None:
            active_bool = active.lower() == "true"
            enrollments = [e for e in enrollments if e.get("active", True) == active_bool]
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        paginated, total = _paginate(enrollments, limit, offset)
        for item in paginated:
            item["courseId"] = course_id
        return jsonify({"results": paginated, "totalCount": total})

    @app.route("/learn/api/public/v1/courses/<course_id>/enrollments", methods=["POST"])
    def create_enrollment(course_id):
        data = request.json
        if "userId" not in data or "role" not in data:
            return jsonify({"message": "Missing userId or role"}), 400
        if course_id not in enrollments_data:
            enrollments_data[course_id] = []
        existing = next((e for e in enrollments_data[course_id] if e["userId"] == data["userId"]), None)
        if existing:
            return jsonify({"message": "User already enrolled"}), 409
        enrollment = {
            "userId": data["userId"],
            "role": data["role"],
            "created": "2023-01-01T00:00:00Z",
            "active": True
        }
        enrollments_data[course_id].append(enrollment)
        enrollment["courseId"] = course_id
        return jsonify(enrollment), 201

    @app.route("/learn/api/public/v1/courses/<course_id>/enrollments/<user_id>", methods=["DELETE"])
    def delete_enrollment(course_id, user_id):
        if course_id not in enrollments_data:
            return jsonify({"message": "Enrollment not found"}), 404
        enrollments = enrollments_data[course_id]
        original_len = len(enrollments)
        enrollments_data[course_id] = [e for e in enrollments if e["userId"] != user_id]
        if len(enrollments_data[course_id]) == original_len:
            return jsonify({"message": "Enrollment not found"}), 404
        return "", 204

    # ---------- ASSIGNMENTS ----------
    @app.route("/learn/api/public/v1/courses/<course_id>/assignments", methods=["GET"])
    def get_assignments(course_id):
        assignments = assignments_data.get(course_id, [])
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        paginated, total = _paginate(assignments, limit, offset)
        for item in paginated:
            item["courseId"] = course_id
        return jsonify({"results": paginated, "totalCount": total})

    @app.route("/learn/api/public/v1/courses/<course_id>/contents/createAssignment", methods=["POST"])
    def create_assignment_via_contents(course_id):
        data = request.json
        if "name" not in data or "points" not in data:
            return jsonify({"message": "Missing name or points"}), 400
        assignment_id = str(uuid.uuid4())
        assignment = {
            "id": assignment_id,
            "courseId": course_id,
            "name": data["name"],
            "description": data.get("description"),
            "dueDate": data.get("dueDate"),
            "points": data["points"],
            "created": "2023-01-01T00:00:00Z",
            "modified": "2023-01-01T00:00:00Z"
        }
        assignments_data.setdefault(course_id, []).append(assignment)
        return jsonify(assignment), 201

    @app.route("/learn/api/public/v1/courses/<course_id>/assignments/<assignment_id>", methods=["PATCH"])
    def patch_assignment(course_id, assignment_id):
        assignments = assignments_data.get(course_id, [])
        assignment = next((a for a in assignments if a["id"] == assignment_id), None)
        if not assignment:
            return jsonify({"message": "Assignment not found"}), 404
        data = request.json
        for key in ["name", "description", "dueDate", "points"]:
            if key in data:
                assignment[key] = data[key]
        assignment["modified"] = "2023-01-02T00:00:00Z"
        return jsonify(assignment)

    # ---------- GRADEBOOK (stub) ----------
    @app.route("/learn/api/public/v2/courses/<course_id>/gradebook/columns", methods=["GET"])
    def get_gradebook_columns(course_id):
        return jsonify({"results": []})

    return app