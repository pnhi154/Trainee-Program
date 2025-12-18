from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register_students():
    try:
        data = request.get_json()

        if not data or "students" not in data:
            return jsonify({
                "status": "error",
                "message": "Dữ liệu không hợp lệ. Vui lòng kiểm tra lại các trường thông tin."
            }), 400

        students = data["students"]

        total_students = len(students)
        seen_ids = set()
        duplicate_students = []
        eligible_students = []

        for student in students:
            required_fields = ["student_id", "name", "age", "gender"]
            for field in required_fields:
                if field not in student:
                    return jsonify({
                        "status": "error",
                        "message": f"Thiếu dữ liệu về {field}"
                    }), 400

            student_id = student["student_id"]
            age = student["age"]

            if not isinstance(age, int):
                return jsonify({
                    "status": "error",
                    "message": "Age phải là số nguyên"
                }), 400

            if student_id in seen_ids:
                duplicate_students.append(student)
            else:
                seen_ids.add(student_id)

            if age < 23:
                if student_id not in [s["student_id"] for s in eligible_students]:
                    eligible_students.append(student)

        return jsonify({
            "status": "success",
            "message": "Danh sách đã được xử lý thành công.",
            "total_students": total_students,
            "duplicate_students": duplicate_students,
            "students_eligible_for_free_ticket": eligible_students
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Lỗi hệ thống"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
