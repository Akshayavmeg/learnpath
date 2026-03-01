from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import init_db, get_db
from auth import login_required, admin_required
from recommendations import get_recommendations
from timetable import generate_timetable
import hashlib, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "learnpath-dev-secret-2024")


# ── Init ───────────────────────────────────────────
with app.app_context():
    init_db()


# ── Auth ───────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        pw_hash  = hashlib.sha256(password.encode()).hexdigest()

        db   = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, pw_hash)
        ).fetchone()

        if user:
            session["user_id"]  = user["id"]
            session["username"] = user["username"]
            session["role"]     = user["role"]

            flash("Welcome back, " + user["username"] + "!", "success")

            if user["role"] == "admin":
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("index"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        pw_hash  = hashlib.sha256(password.encode()).hexdigest()

        db = get_db()

        try:
            db.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'student')",
                (username, pw_hash)
            )
            db.commit()

            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))

        except Exception:
            flash("Username already exists.", "error")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You've been logged out.", "info")
    return redirect(url_for("login"))


# ── FIXED: Home redirect ───────────────────────────
@app.route("/")
def home():
    if "user_id" in session:
        if session.get("role") == "admin":
            return redirect(url_for("dashboard"))
        return redirect(url_for("index"))
    return redirect(url_for("login"))


# ── ADDED: Student main page route (THIS WAS MISSING) ──
@app.route("/index")
@login_required
def index():
    return render_template("index.html")


# ── Recommendation ─────────────────────────────────
@app.route("/recommend", methods=["POST"])
@login_required
def recommend():

    name    = request.form.get("name", "").strip()
    grade   = request.form.get("grade", "")
    subject = request.form.get("subject", "Mathematics")
    goal    = request.form.get("goal", "Improve grades")
    style   = request.form.get("style", "Visual")

    data      = get_recommendations(name, grade, subject, goal, style)
    timetable = generate_timetable(subject, style, goal)

    db = get_db()

    existing = db.execute(
        "SELECT id FROM students WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    if existing:

        db.execute(
            """UPDATE students
               SET name=?, grade=?, weak_subject=?, learning_goal=?, learning_style=?, updated_at=CURRENT_TIMESTAMP
               WHERE user_id=?""",
            (name, grade, subject, goal, style, session["user_id"])
        )

        student_id = existing["id"]

    else:

        cur = db.execute(
            """INSERT INTO students
               (user_id, name, grade, weak_subject, learning_goal, learning_style)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (session["user_id"], name, grade, subject, goal, style)
        )

        student_id = cur.lastrowid


    db.execute(
        "DELETE FROM timetable WHERE student_id = ?",
        (student_id,)
    )


    for slot in timetable:

        db.execute(
            """INSERT INTO timetable
               (student_id, day, time_slot, activity, subject)
               VALUES (?, ?, ?, ?, ?)""",
            (
                student_id,
                slot["day"],
                slot["time"],
                slot["activity"],
                slot["subject"]
            )
        )


    db.commit()

    session["student_id"] = student_id

    return render_template(
        "recommendation.html",
        **data,
        timetable=timetable
    )


# ── Admin Dashboard ───────────────────────────────
@app.route("/admin")
@admin_required
def dashboard():

    db = get_db()

    students = db.execute("""
        SELECT s.*, u.username,
               COUNT(p.id) as log_count,
               COALESCE(AVG(p.score),0) as avg_score
        FROM students s
        JOIN users u ON u.id = s.user_id
        LEFT JOIN progress_logs p ON p.student_id = s.id
        GROUP BY s.id
        ORDER BY s.updated_at DESC
    """).fetchall()


    total_students = db.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]


    total_logs = db.execute(
        "SELECT COUNT(*) FROM progress_logs"
    ).fetchone()[0]


    avg_score_row = db.execute(
        "SELECT COALESCE(AVG(score),0) FROM progress_logs"
    ).fetchone()


    avg_score = round(avg_score_row[0], 1)


    subject_dist = db.execute("""
        SELECT weak_subject, COUNT(*) as cnt
        FROM students
        GROUP BY weak_subject
    """).fetchall()


    style_dist = db.execute("""
        SELECT learning_style, COUNT(*) as cnt
        FROM students
        GROUP BY learning_style
    """).fetchall()


    return render_template(
        "admin.html",
        students=students,
        total_students=total_students,
        total_logs=total_logs,
        avg_score=avg_score,
        subject_dist=subject_dist,
        style_dist=style_dist
    )


if __name__ == "__main__":
    app.run(debug=True)