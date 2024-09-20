from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

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
    candidates = [
        {'name': 'Alice', 'id': 1},
        {'name': 'Bob', 'id': 2},
        {'name': 'Charlie', 'id': 3}
    ]
    return render_template('voting.html.jinja', candidates=candidates)

if __name__ == '__main__':
    app.run(debug=True)
