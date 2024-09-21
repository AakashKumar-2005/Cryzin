from flask import Flask, render_template, request, redirect, session, jsonify
from blockchain import Blockchain
from config import GENESIS
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key
blockchain = Blockchain()

AUTH_ADDRESS = os.environ.get('AUTH_ADDRESS', 'http://localhost:8000')

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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.jinja', auth=AUTH_ADDRESS)

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
    app.run(debug=True, host="0.0.0.0")
