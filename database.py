import sqlite3

DB_NAME = "students.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
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
    """List students with optional filters."""
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


if __name__ == "__main__":
    init_db()
    print("Database created successfully: students.db")