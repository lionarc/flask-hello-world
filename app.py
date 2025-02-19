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
    "Welche Mahlzeit genießt du am meisten?",
    "Wie machst du am liebsten Urlaub?",
    "Was ist dir bei Filmen wichtig?",
    "Was machst du am liebsten draußen?",
    "Was entspannt dich am meisten?",
    "Auf welche Jahreszeit freust du dich am meisten?",
    "Für welches Haustier würdest du dich entscheiden?",
    "Was schätzt du am meisten in Beziehungen?",
    "Welchen Snack kaufst du am häufigsten?"
]
answers = [
    ["Frühstück", "Brunch", "Mittagessen", "Abendessen", "Late-Night-Snack"],
    ["Strandurlaub", "Stadterkundung", "Abenteuerreise", "Kulturelles Eintauchen", "auf der eigenen Couch"],
    ["viel Action & Spannung", "möglichst indpendent", "die meisten Oscars", "Bechdel-Test bestehen", "ist oder wird ein Klassiker"],
    ["Wandern", "Fahrradfahren", "im Freien schlafen", "am See chillen", "Picknicken"],
    ["Ein Buch lesen", "Musik hören", "Meditation", "Serien schauen", "Badewanne"],
    ["Sommer", "Herbst", "Winter", "Frühling", "Ich liebe sie alle!"],
    ["Hund", "Katze", "Schlange", "Aquarium voller Fische und Seetiere", "Schildkröte", "bloß kein Tier im Haus"],
    ["gemeinsamer Humor", "Vertrauen", "Intimität", "ähnliche Interessen", "gegenseitige Unterstützung"],
    ["Chips", "Schokolade", "Kekse", "Nüsse", "Obst"]
]
# Define the songs and their paths
songs = {
    '100': "static/Dilemma (Lyrics) - Nelly  ft. Kelly Rowland.mp3",
    '90': "static/Kylie Minogue - Cant Get You Out Of My Head (Official Video).mp3",
    '80': "static/Serge Gainsbourg & Jane Birkin - Je t'aime... moi non plus_Original videoclip (Fontana 1969).mp3",
    '70': "static/John Paul Young - Love Is In The Air (1978).mp3",
    '60': "static/Sinéad OConnor - Nothing Compares 2 U (Official Music Video) [HD].mp3",
    '50': "static/Marianne Rosenberg Er gehrt zu mir.mp3",
    '40': "static/Every Breath You Take.mp3",
    '30': "static/wo bist du mein sonnenlicht grup tekkan.mp3",
    '20': "static/Vom selben Stern Radio Edit.mp3",
    '10': "static/Regen und Meer.mp3",
    '1': "static/Creep - Radiohead (Lyrics).mp3",
    '0': "static/game-over-arcade-6435.mp3",
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
        match_data = calculate_match_percentage(person1_data, person2_data)
        match_percentage = match_data[0]
        matched_answers = match_data[1]
        if match_percentage >= 50:
            result = "Congratulations! You have more than 50% in common!"
        else:
            result = "Sorry, you have less than 50% in common."
        
        return render_template('result.html', person1_data=person1_data, person2_data=person2_data, match_percentage=match_percentage, song_path=get_song_path(match_percentage), matched_answers=matched_answers, source='person1')
    else:
        return render_template('waiting_screen.html')

@app.route('/result_person2')
def result_person2():
    if submission_status['person1'] and submission_status['person2']:
        match_data = calculate_match_percentage(person1_data, person2_data)
        match_percentage = match_data[0]
        matched_answers = match_data[1]
        if match_percentage >= 50:
            result = "Congratulations! You have more than 50% in common!"
        else:
            result = "Sorry, you have less than 50% in common."
        
        return render_template('result.html', person1_data=person1_data, person2_data=person2_data, match_percentage=match_percentage, song_path=get_song_path(match_percentage), matched_answers=matched_answers, source='person2')
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
    match_percentage = (match_count / total_questions) * 100

    # Find the matched answers
    matched_answers = {}
    for question in questions:
        if person1_data.get(question) == person2_data.get(question):
            matched_answers[question] = person1_data.get(question)

    return match_percentage, matched_answers

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
    elif match_percentage >= 50:
        return songs['50']
    elif match_percentage >= 40:
        return songs['40']
    elif match_percentage >= 30:
        return songs['30']
    elif match_percentage >= 20:
        return songs['20']
    elif match_percentage >= 10:
        return songs['10']
    elif match_percentage > 0:
        return songs['1']
    elif match_percentage == 0:
        return songs['0']
    else:
        return songs['0']

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)








