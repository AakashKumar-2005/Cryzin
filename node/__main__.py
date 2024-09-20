from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from blockchain import Blockchain
from config import GENESIS

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key
blockchain = Blockchain()

DEFAULT_PORT = 3000
ROOT_NODE_ADDRESS = f"http://localhost:{DEFAULT_PORT}"

@app.route("/api/blocks", methods=["GET", "POST"])
def blocks():
    return jsonify([block.__dict__() for block in blockchain.chain])


@app.route("/api/mine", methods=["POST"])
def mine():
    data = request.json
    print(type(data), data)
    blockchain.add_block(data=data)
    return redirect("/api/blocks")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        if voter_id:
            session['voter_id'] = voter_id
            return redirect(url_for('voting'))
    return render_template('index.html.jinja')

@app.route('/voting', methods=['GET'])
def voting():
    voter = session['voter_id']
    return render_template('voting.html.jinja', candidates=GENESIS, voter=voter)

@app.route('/results', methods=["GET", "POST"])
def results():
    votes = {}
    for block in blockchain.chain[1:]:
        for vote in block.data:
            if vote["candidate"] not in votes.keys():
                votes[vote["candidate"]] = 0
            votes[vote["candidate"]] += 1
    return render_template('results.html.jinja', votes=votes)


if __name__ == "__main__":
    app.run(debug=True)
