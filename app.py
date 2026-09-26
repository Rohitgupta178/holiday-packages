from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re


app = Flask(__name__)

DATABASE = "contacts.db"


def init_db():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    # Required-field validation
    if not name or not email or not message:
        return render_template(
            "error.html",
            message="Please fill in all fields."
        ), 400

    # Email validation
    if not is_valid_email(email):
        return render_template(
            "error.html",
            message="Please enter a valid email address."
        ), 400

    # Save inquiry
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO contacts (name, email, message)
        VALUES (?, ?, ?)
        """,
        (name, email, message)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)