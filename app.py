from flask import Flask, request, render_template_string

app = Flask(__name__)

# In-memory data storage
workouts = []

# Calorie calculation function
def calculate_calories(exercise_type, duration_minutes, weight_kg):
    met_values = {
        "running": 9.8,
        "cycling": 7.5,
        "weightlifting": 6.0,
        "walking": 3.8,
        "yoga": 3.0,
        "jump rope": 12.0
    }
    met = met_values.get(exercise_type.lower(), 5.0)
    duration_hours = duration_minutes / 60
    return round(met * weight_kg * duration_hours, 2)

# Home route with form
@app.route('/')
def home():
    return '''
    <h1>Fitness Tracker</h1>
    <form action="/submit" method="post">
        <label for="name">Name:</label><br>
        <input type="text" id="name" name="name" placeholder="Your name"><br><br>

        <label for="weight">Your Weight (kg):</label><br>
        <input type="number" id="weight" name="weight" step="0.1"><br><br>

        <label for="date">Date:</label><br>
        <input type="date" id="date" name="date"><br><br>

        <label for="exercise">Exercise:</label><br>
        <input type="text" id="exercise" name="exercise" placeholder="e.g. Running"><br><br>

        <label for="duration">Duration (minutes):</label><br>
        <input type="number" id="duration" name="duration"><br><br>

        <button type="submit">Submit Workout</button>
    </form>
    <br>
    <a href="/workouts">View Workout History</a>
    '''

# Submit form data and store
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    date = request.form['date']
    exercise = request.form['exercise']
    duration = float(request.form['duration'])
    weight = float(request.form['weight'])

    calories = calculate_calories(exercise, duration, weight)

    data = {
        'name': name,
        'date': date,
        'exercise': exercise,
        'duration': duration,
        'calories': calories
    }
    workouts.append(data)

    return f"Workout added! Calories burned: {calories} <br><a href='/'>Back to Home</a> | <a href='/workouts'>View Workouts</a>"

# Display all workouts in table
@app.route('/workouts')
def show_workouts():
    table_html = '''
    <h2>Workout History</h2>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Name</th>
            <th>Date</th>
            <th>Exercise</th>
            <th>Duration (minutes)</th>
            <th>Calories Burned</th>
        </tr>
    '''
    for w in workouts:
        table_html += f'''
        <tr>
            <td>{w["name"]}</td>
            <td>{w["date"]}</td>
            <td>{w["exercise"]}</td>
            <td>{w["duration"]}</td>
            <td>{w["calories"]}</td>
        </tr>
        '''
    table_html += '</table><br><a href="/">Back to Home</a>'
    return table_html

if __name__ == '__main__':
    app.run(debug=True)