from flask import Flask, request, render_template, jsonify

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
    return render_template('index.html')

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
    return render_template('workouts.html', workouts=workouts)

@app.route('/user/<name>')
def user_detail(name):
    person_workouts = [w for w in workouts if w['name'].lower() == name.lower()]
    if not person_workouts:
        return f"No data found for {name}. <a href='/'>Back</a>"

    dates = [w['date'] for w in person_workouts]
    calories = [w['calories'] for w in person_workouts]
    
    return render_template('user_graph.html', name=name, dates=dates, calories=calories)

if __name__ == '__main__':
    app.run(debug=True)
