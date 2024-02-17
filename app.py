import time
from flask import Flask, render_template, request, redirect, url_for


# Create a Flask application
app = Flask(__name__)

person1_data = {}
person2_data = {}
submission_status = {
    'person1': False,
    'person2': False
}

# Define the questions
questions = [
    "What is your favorite meal of the day?",
    "Which cuisine do you enjoy the most?",
    "What is your preferred dessert?",
    "Which snack do you crave the most?",
    "What is your go-to comfort food?"
]
answers = [
    ["Breakfast", "Brunch", "Lunch", "Dinner", "Late-night snack"],
    ["Italian", "Mexican", "Japanese", "Indian", "American"],
    ["Chocolate cake", "Ice cream", "Cheesecake", "Fruit tart", "Cookies"],
    ["Popcorn", "Potato chips", "Nachos", "Chocolate", "Trail mix"],
    ["Pizza", "Mac and cheese", "Fried chicken", "Grilled cheese", "Pasta"]
]
# Define the songs and their paths
songs = {
    '100': "static/Die Eine.mp3",
    '90': "static/Every Breath You Take.mp3",
    '80': "static/Ben E King Stand By Me Lyrics.mp3",
    '70': "static/Vom selben Stern Radio Edit.mp3",
    '60': "static/Serge Gainsbourg & Jane Birkin - Je t'aime... moi non plus_Original videoclip (Fontana 1969).mp3",
    'default': "static/Tina Turner What s Love Got To Do With It Lyrics.mp3"
}

reset_flag = False

@app.route('/')
def start_screen():
    person1_data = {}
    person2_data = {}
    reset_flag = False
    submission_status = {
    'person1': False,
    'person2': False}
    return render_template('start_screen.html')

# Routes for Person 1 and Person 2
@app.route('/person1')
def person1_form():
    # if submission_status['person1']:
    #     return redirect(url_for('result'))
    return render_template('questionnaire.html', questions=questions, answers=answers, submit_route='/submit_person1')

@app.route('/person2')
def person2_form():
    # if submission_status['person2']:
    #     return redirect(url_for('result'))
    return render_template('questionnaire.html', questions=questions, answers=answers, submit_route='/submit_person2')

@app.route('/submit_person1', methods=['POST'])
def submit_person1():
    global person1_data, submission_status
    # Process form data for Person 1
    person1_data = request.form.to_dict()
    submission_status['person1'] = True
    # Check if both persons have submitted data
    # if submission_status['person1'] and submission_status['person2']:
    #     return redirect(url_for('result_person1', source='person1'))  # Redirect ∏o the result route
    # else:
    return redirect(url_for('waiting_screen', source='person1'))   # Redirect to the waiting screen route

@app.route('/submit_person2', methods=['POST'])
def submit_person2():
    global person2_data, submission_status
    # Process form data for Person 2
    person2_data = request.form.to_dict()
    submission_status['person2'] = True
    # Check if both persons have submitted data
    # if submission_status['person1'] and submission_status['person2']:
    #     return redirect(url_for('result_person2', source='person2'))  # Redirect to the result route
    # else:
    return redirect(url_for('waiting_screen', source='person2'))  # Redirect to the waiting screen route


# Separate result routes for person 1 and person 2
@app.route('/result_person1')
def result_person1():
    if submission_status['person1'] and submission_status['person2']:
        match_percentage = calculate_match_percentage(person1_data, person2_data)
        if match_percentage >= 50:
            result = "Congratulations! You have more than 50% in common!"
        else:
            result = "Sorry, you have less than 50% in common."
        
        return render_template('result.html', person1_data=person1_data, person2_data=person2_data, match_percentage=match_percentage, song_path=get_song_path(match_percentage), source='person1')
    else:
        return render_template('waiting_screen.html')

@app.route('/result_person2')
def result_person2():
    if submission_status['person1'] and submission_status['person2']:
        match_percentage = calculate_match_percentage(person1_data, person2_data)
        if match_percentage >= 50:
            result = "Congratulations! You have more than 50% in common!"
        else:
            result = "Sorry, you have less than 50% in common."
        
        return render_template('result.html', person1_data=person1_data, person2_data=person2_data, match_percentage=match_percentage, song_path=get_song_path(match_percentage), source='person2')
    else:
        return render_template('waiting_screen.html')
    
@app.route('/waiting_screen')
def waiting_screen():
    global submission_status, reset_flag
    source = request.args.get('source')
    print(reset_flag)
    # Check if both persons have submitted their questionnaires
    if submission_status['person1'] and submission_status['person2'] and not reset_flag:
        if source == 'person1':
            return redirect(url_for('result_person1'))
        elif source == 'person2':
            return redirect(url_for('result_person2'))
    elif reset_flag: #not submission_status['person1'] and not submission_status['person2']:
        return reset()
        
    return render_template('waiting_screen.html')


@app.route('/reset')
def reset():
    global person1_data, person2_data, submission_status, reset_flag
    source = request.args.get('source') 
    reset_flag = not reset_flag  # Toggle the reset flag
    # Reset the data and submission status
    if source == 'person1':
        person1_data = {}
        submission_status['person1'] = False
    elif source == 'person2':
        person2_data = {}
        submission_status['person2'] = False

    if source == 'person1':
        return redirect(url_for('person1_form'))
    elif source == 'person2':
        return redirect(url_for('person2_form'))
    else:
        # Handle the case if person is None or invalid
        # Redirect to a default route or display an error message
        return redirect(url_for('waiting_screen'))  # For example, redirect to the index page

def calculate_match_percentage(person1_data, person2_data):
    total_questions = len(questions)
    match_count = sum(1 for q in questions if person1_data.get(q) == person2_data.get(q))
    return (match_count / total_questions) * 100

def get_song_path(match_percentage):
    if match_percentage >= 100:
        return songs['100']
    elif match_percentage >= 90:
        return songs['90']
    elif match_percentage >= 80:
        return songs['80']
    elif match_percentage >= 70:
        return songs['70']
    elif match_percentage >= 60:
        return songs['60']
    else:
        return songs['default']

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)








