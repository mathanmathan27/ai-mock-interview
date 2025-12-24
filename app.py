from flask import Flask, render_template, redirect, url_for, request, session
import smtplib
from email.message import EmailMessage
import json
import os

app = Flask(__name__)
app.secret_key = "secure_key_123"

USERS_FILE = "users.json"

# -------------------------------
# USER STORAGE FUNCTIONS
# -------------------------------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Load users at startup
USERS = load_users()

# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------------
# LOGIN
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"].strip()
        p = request.form["password"].strip()

        if USERS.get(u) == p:
            session["user"] = u
            return redirect(url_for("home"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# -------------------------------
# REGISTER
# -------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"].strip()
        p = request.form["password"].strip()

        if u in USERS:
            return render_template("register.html", error="Username already exists")

        USERS[u] = p
        save_users(USERS)
        return redirect(url_for("login"))

    return render_template("register.html")

# -------------------------------
# LOGOUT
# -------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# -------------------------------
# INTERVIEW
# -------------------------------
@app.route("/interview")
def interview():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("interview.html")

# -------------------------------
# RESULT  ✅ (THIS WAS MISSING)
# -------------------------------
@app.route("/result")
def result():
    # Results are stored in localStorage (frontend)
    # This page just renders the result UI
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("result.html")

# -------------------------------
# CONTACT (EMAIL)
# -------------------------------
@app.route("/contact_us", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        user_email = request.form["email"]
        message = request.form["message"]

        msg = EmailMessage()
        msg["Subject"] = "AI Mock Interview - Contact Query"
        msg["From"] = "yourgmail@gmail.com"
        msg["To"] = "yourgmail@gmail.com"
        msg.set_content(f"From: {user_email}\n\nMessage:\n{message}")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login("yourgmail@gmail.com", "YOUR_APP_PASSWORD")
                smtp.send_message(msg)
            return render_template(
                "contact_us.html",
                success="Message sent successfully"
            )
        except Exception as e:
            return render_template(
                "contact_us.html",
                error=str(e)
            )

    return render_template("contact_us.html")

# -------------------------------
# PERFORMANCE / REPORT
# -------------------------------
@app.route("/performance")
def performance():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("performance.html")

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
