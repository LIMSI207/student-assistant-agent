import sqlite3
import csv
import os

DB_NAME = "students.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create database tables if they do not exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Active'
            )
        """)


def add_student(name: str, department: str, status: str = "Active") -> dict:
    """Add a student to the database."""
    if not name.strip() or not department.strip() or not status.strip():
        return {"error": "Name, department and status are required."}

    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO students (name, department, status) VALUES (?, ?, ?)",
            (name.strip(), department.strip(), status.strip())
        )
        return {"message": "Student added", "id": cur.lastrowid}


def search_student(name: str) -> list:
    """Search students by name."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM students WHERE name LIKE ? ORDER BY id",
            (f"%{name.strip()}%",)
        ).fetchall()
        return [dict(row) for row in rows]


def list_students(department: str = "", status: str = "") -> list:
    """List students with optional department and status filters."""
    sql = "SELECT * FROM students WHERE 1=1"
    params = []

    if department:
        sql += " AND LOWER(department) = LOWER(?)"
        params.append(department.strip())

    if status:
        sql += " AND LOWER(status) = LOWER(?)"
        params.append(status.strip())

    sql += " ORDER BY id"

    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]


def count_students(department: str = "", status: str = "") -> int:
    """Count students with optional filters."""
    sql = "SELECT COUNT(*) FROM students WHERE 1=1"
    params = []

    if department:
        sql += " AND LOWER(department) = LOWER(?)"
        params.append(department.strip())

    if status:
        sql += " AND LOWER(status) = LOWER(?)"
        params.append(status.strip())

    with get_connection() as conn:
        return conn.execute(sql, params).fetchone()[0]


def update_student(
    student_id: int,
    name: str = "",
    department: str = "",
    status: str = ""
) -> dict:
    """Update a student by ID."""
    changes = {
        key: value.strip()
        for key, value in {
            "name": name,
            "department": department,
            "status": status
        }.items()
        if value.strip()
    }

    if not changes:
        return {"error": "Provide a field to update."}

    with get_connection() as conn:
        exists = conn.execute(
            "SELECT id FROM students WHERE id = ?", (student_id,)
        ).fetchone()

        if not exists:
            return {"error": "Student ID not found."}

        assignments = ", ".join(f"{key} = ?" for key in changes)
        values = list(changes.values()) + [student_id]

        conn.execute(
            f"UPDATE students SET {assignments} WHERE id = ?", values
        )
        return {"message": "Student updated", "id": student_id}


def delete_student(student_id: int) -> dict:
    """Delete a student by ID."""
    with get_connection() as conn:
        cur = conn.execute(
            "DELETE FROM students WHERE id = ?", (student_id,)
        )

        if cur.rowcount == 0:
            return {"error": "Student ID not found."}

        return {"message": "Student deleted", "id": student_id}


def get_student_statistics() -> dict:
    """Get total, active, inactive and department-wise statistics."""
    with get_connection() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        active = conn.execute(
            "SELECT COUNT(*) FROM students WHERE LOWER(status) = 'active'"
        ).fetchone()[0]

        inactive = conn.execute(
            "SELECT COUNT(*) FROM students WHERE LOWER(status) = 'inactive'"
        ).fetchone()[0]

        departments = conn.execute("""
            SELECT
                department,
                COUNT(*) AS total_students,
                SUM(CASE WHEN LOWER(status) = 'active'
                    THEN 1 ELSE 0 END) AS active_students,
                SUM(CASE WHEN LOWER(status) = 'inactive'
                    THEN 1 ELSE 0 END) AS inactive_students
            FROM students
            GROUP BY LOWER(department)
            ORDER BY total_students DESC, LOWER(department)
        """).fetchall()

        department_stats = [dict(row) for row in departments]

        return {
            "total_students": total,
            "active_students": active,
            "inactive_students": inactive,
            "department_count": len(department_stats),
            "department_stats": department_stats
        }


def export_students_csv(filename="students_report.csv"):
    if not filename.lower().endswith(".csv"):
        return {"error": "Filename must end with .csv"}

    if os.path.basename(filename) != filename:
        return {"error": "Invalid filename."}

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, name, department, status
            FROM students
            ORDER BY id
        """).fetchall()

    try:
        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            writer.writerow([
                "ID", "Name", "Department", "Status"
            ])

            for row in rows:
                writer.writerow([
                    row["id"],
                    row["name"],
                    row["department"],
                    row["status"]
                ])

        return {
            "message": "CSV export successful",
            "filename": filename,
            "records_exported": len(rows)
        }

    except OSError as error:
        return {"error": str(error)}
def update_student_by_name(
    old_name,
    name="",
    department="",
    status=""
):
    old_name = old_name.strip()

    if not old_name:
        return {"error": "Student name is required."}

    changes = {
        key: value.strip()
        for key, value in {
            "name": name,
            "department": department,
            "status": status
        }.items()
        if value.strip()
    }

    if not changes:
        return {"error": "Provide a field to update."}

    with get_connection() as conn:
        students = conn.execute(
            "SELECT id FROM students WHERE LOWER(name) = LOWER(?)",
            (old_name,)
        ).fetchall()

        if len(students) == 0:
            return {"error": "Student not found."}

        if len(students) > 1:
            return {
                "error": "Multiple students found. Please update using Student ID."
            }

        student_id = students[0]["id"]

        assignments = ", ".join(
            f"{key} = ?" for key in changes
        )

        conn.execute(
            f"UPDATE students SET {assignments} WHERE id = ?",
            list(changes.values()) + [student_id]
        )

        return {
            "message": "Student updated successfully.",
            "id": student_id
        }


def delete_student_by_name(name):
    name = name.strip()

    if not name:
        return {"error": "Student name is required."}

    with get_connection() as conn:
        students = conn.execute(
            "SELECT id FROM students WHERE LOWER(name) = LOWER(?)",
            (name,)
        ).fetchall()

        if len(students) == 0:
            return {"error": "Student not found."}

        if len(students) > 1:
            return {
                "error": "Multiple students found. Please delete using Student ID."
            }

        student_id = students[0]["id"]

        conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        return {
            "message": "Student deleted successfully.",
            "id": student_id
        }


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully: students.db")