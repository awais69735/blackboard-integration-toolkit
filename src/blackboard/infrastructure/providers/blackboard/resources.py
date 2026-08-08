"""Blackboard REST API endpoint constants (aligned with latest API)."""

BASE_PATH = "/learn/api/public"

# Users (v1) - unchanged
USERS = f"{BASE_PATH}/v1/users"

# Courses (v3) - upgraded
COURSES = f"{BASE_PATH}/v3/courses"

# Enrollments (v1) - unchanged
ENROLLMENTS = f"{BASE_PATH}/v1/courses/{{course_id}}/enrollments"

# Assignments - list and update still use v1
ASSIGNMENTS = f"{BASE_PATH}/v1/courses/{{course_id}}/assignments"

# New: create assignment via contents endpoint
CREATE_ASSIGNMENT = f"{BASE_PATH}/v1/courses/{{course_id}}/contents/createAssignment"

# Gradebook (v2) - for future implementation
GRADEBOOK_COLUMNS = f"{BASE_PATH}/v2/courses/{{course_id}}/gradebook/columns"