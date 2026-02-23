

from flask import Flask, request, jsonify, send_from_directory, redirect, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import mariadb
import os

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "Frontend")

# Serve everything from Frontend/ as static:
# /images/x.png -> Frontend/images/x.png
# /logare/log.html -> Frontend/logare/log.html
# /dashboard/dsh.html -> Frontend/dashboard/dsh.html
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# Needed for sessions (login)
app.secret_key = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_123456789"

# ---------------- DB ----------------
def db_conn():
    return mariadb.connect(
        user="root",
        password="Eu beau apa",
        host="localhost",
        port=3306,
        database="liceu_app"
    )

def is_logged_in():
    return session.get("user_id") is not None

# ---------------- Pages ----------------
@app.route("/")
def root():
    return redirect("/dashboard") if is_logged_in() else redirect("/login")

@app.route("/login")
def login_page():
    return send_from_directory(FRONTEND_DIR, "logare/log.html")

@app.route("/dashboard")
def dashboard_page():
    if not is_logged_in():
        return redirect("/login")
    return send_from_directory(FRONTEND_DIR, "dashboard/dsh.html")

# ---------------- AUTH APIs ----------------
@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}

    nume = (data.get("nume") or "").strip()
    email = (data.get("email") or "").strip()
    parola = data.get("parola") or ""

    clasa = (data.get("clasa") or "").strip()
    liceul = (data.get("liceul") or "").strip()
    profil = (data.get("profil") or "").strip()  # optional

    if not nume or not email or not parola:
        return jsonify({"error": "nume, email, parola are required"}), 400

    parola_hash = generate_password_hash(parola)

    conn = db_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO elevi (nume, email, parola, clasa, liceul, data_inscriere)
            VALUES (?, ?, ?, ?, ?, NOW())
        """, (nume, email, parola_hash, clasa, liceul,))
        conn.commit()
    except mariadb.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409
    finally:
        conn.close()

    return jsonify({"ok": True})

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    parola = data.get("parola") or ""

    if not email or not parola:
        return jsonify({"error": "email and parola required"}), 400

    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id_elev, nume, parola FROM elevi WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Wrong email or password"}), 401

    user_id, nume, parola_hash = row

    if not check_password_hash(parola_hash, parola):
        return jsonify({"error": "Wrong email or password"}), 401

    session["user_id"] = user_id
    session["nume"] = nume
    session["email"] = email

    return jsonify({"ok": True, "redirect": "/dashboard"})

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True, "redirect": "/login"})

@app.route("/api/me", methods=["GET"])
def api_me():
    if not is_logged_in():
        return jsonify({"error": "not logged in"}), 401
    return jsonify({
        "id_elev": session["user_id"],
        "nume": session.get("nume"),
        "email": session.get("email")
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
