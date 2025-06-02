# api/index.py

from flask import Flask, request, render_template, redirect
from flask_cors import CORS
import mysql.connector
from flask import send_from_directory
import os

app = Flask(__name__, template_folder="../templates")
CORS(app)

# MySQL connection
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
    cursor.execute("SELECT date, duration, weight FROM workouts WHERE name = %s ORDER BY date ASC", (name,))
    data = cursor.fetchall()
    dates = [str(row[0]) for row in data]
    durations = [row[1] for row in data]
    weights = [row[2] for row in data]
    return render_template('user_graph.html', user=name, dates=dates, durations=durations, weights=weights)

# Export app for Vercel
def handler(request, response):
    return app(request.environ, response.start_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

