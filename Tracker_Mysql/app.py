from flask import Flask, render_template, request, redirect
import mysql.connector
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()  # Load values from .env
app = Flask(__name__)

# Connect to MySQL
try:
    db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 8000)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = db.cursor()
    print("✅ MySQL connection successful.")
except mysql.connector.Error as err:
    print("❌ Error connecting to MySQL:", err)

    
# Create table (run once or ensure exists)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        date DATE,
        exercise VARCHAR(100),
        duration INT,
        weight FLOAT
    )
""")
db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    date = request.form['date']
    exercise = request.form['exercise']
    duration = request.form['duration']
    weight = request.form['weight'] or None

    query = "INSERT INTO workouts (name, date, exercise, duration, weight) VALUES (%s, %s, %s, %s, %s)"
    values = (name, date, exercise, duration, weight)
    cursor.execute(query, values)
    db.commit()

    return redirect('/workouts')

@app.route('/workouts')
def workouts():
    cursor.execute("SELECT name, date, exercise, duration, weight FROM workouts ORDER BY date DESC")
    data = cursor.fetchall()
    workouts = [
        {"name": row[0], "date": row[1], "exercise": row[2], "duration": row[3], "weight": row[4]}
        for row in data
    ]
    return render_template('workouts.html', workouts=workouts)

@app.route('/user/<string:name>')
def user_graph(name):
    cursor.execute("""
        SELECT date, duration, weight
        FROM workouts
        WHERE name = %s
        ORDER BY date ASC
    """, (name,))
    data = cursor.fetchall()

    dates = [str(row[0]) for row in data]
    durations = [row[1] for row in data]
    weights = [row[2] for row in data]

    return render_template('user_graph.html', user=name, dates=dates, durations=durations, weights=weights)




def handler(environ, start_response):
    return app(environ, start_response)


if __name__ == '__main__':
    app.run(debug=True)
