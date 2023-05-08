from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_bcrypt import Bcrypt

# setting up application
app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route("/home")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, city, email, password FROM users')
    records = cur.fetchall()
    conn.close()

    return render_template('index.html', records=records)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        try:
            # Execute an INSERT statement to add the user data to the 'users' table
            conn.execute('INSERT INTO users(name, city, email, password) VALUES (?,?,?,?)',
                         (name, city, email, bcrypt.generate_password_hash(password)))

            conn.commit()

        except Exception as dbError:
            print(f"Error writing to DB: {dbError}")
            conn.rollback()

        conn.close()
        return redirect(url_for('login'))

    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cur.fetchone()
        conn.close()

        if user is not None and bcrypt.check_password_hash(user['password'], password):
            # The email and password match, so log in the user
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            # The email and password do not match, so display an error message
            error = 'Invalid email or password'
            return render_template('index.html', error=error)

    return render_template("index.html")


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    # Allows you to access query results as if they were a dictionary
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == '__main__':
    app.run(debug=True)
