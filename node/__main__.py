
"""
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Global candidates list
candidates = [
    {'name': 'Alice', 'id': 1},
    {'name': 'Bob', 'id': 2},
    {'name': 'Charlie', 'id': 3}
]

# Store votes in a dictionary
votes = {candidate['id']: 0 for candidate in candidates}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        if voter_id:
            session['voter_id'] = voter_id
            return redirect(url_for('voting'))
    return render_template('index.html.jinja')

@app.route('/voting')
def voting():
    return render_template('voting.html.jinja', candidates=candidates)

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    candidate_id = int(request.form['candidate_id'])
    if candidate_id in votes:
        votes[candidate_id] += 1  # Increment the vote count
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('results.html.jinja', candidates=candidates, votes=votes)

if __name__ == '__main__':
    app.run(debug=True)

"""
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Initialize a global variable to keep track of votes
votes = {
    1: 0,  # Votes for Alice
    2: 0,  # Votes for Bob
    3: 0   # Votes for Charlie
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        if voter_id:
            session['voter_id'] = voter_id
            return redirect(url_for('voting'))
    return render_template('index.html.jinja')

@app.route('/voting', methods=['GET', 'POST'])
def voting():
    if request.method == 'POST':
        candidate_id = int(request.form['candidate_id'])
        if candidate_id in votes:
            votes[candidate_id] += 1  # Increment the vote count for the selected candidate
            return redirect(url_for('results'))  # Redirect to results after voting

    candidates = [
        {'name': 'Alice', 'id': 1},
        {'name': 'Bob', 'id': 2},
        {'name': 'Charlie', 'id': 3}
    ]
    return render_template('voting.html.jinja', candidates=candidates)

@app.route('/results')
def results():
    candidates = [
        {'name': 'Alice', 'id': 1, 'votes': votes[1]},
        {'name': 'Bob', 'id': 2, 'votes': votes[2]},
        {'name': 'Charlie', 'id': 3, 'votes': votes[3]}
    ]
    return render_template('results.html.jinja', candidates=candidates)


if __name__ == "__main__":
    app.run(debug=True)
