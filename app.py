
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask("app")

# Create database and table if not exists
def init_db():
    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        amount REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# HTML template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Yves Capital Loans</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            padding: 40px;
        }
        .container {
            background: white;
            padding: 30px;
            max-width: 500px;
            margin: auto;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
        }
        button {
            margin-top: 15px;
            width: 100%;
            padding: 10px;
            background: #0a7cff;
            color: white;
            border: none;
            font-size: 16px;
        }
        .success {
            color: green;
            text-align: center;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Yves Capital Loans</h1>

    {% if success %}
        <p class="success">Application submitted successfully!</p>
    {% endif %}

    <form method="POST" action="/apply">
        <label>Full Name</label>
        <input type="text" name="name" required>

        <label>Phone Number</label>
        <input type="text" name="phone" required>

        <label>Loan Amount</label>
        <input type="number" name="amount" required>

        <button type="submit">Apply for Loan</button>
    </form>
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE, success=False)

@app.route("/apply", methods=["POST"])
def apply():
    name = request.form["name"]
    phone = request.form["phone"]
    amount = request.form["amount"]

    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO applications (name, phone, amount) VALUES (?, ?, ?)",
        (name, phone, amount)
    )

    conn.commit()
    conn.close()

    return render_template_string(HTML_PAGE, success=True)


if __name__ == "__main__":
    app.run(debug=True)