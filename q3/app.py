import json
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


def db_connection():
    conn = sqlite3.connect('database/voting_system.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/result/')
def result():
    conn = db_connection()
    count_vote = conn.execute('''
    SELECT  candidate_id,
            count(*) AS num_vote
    FROM vote
    GROUP BY candidate_id
    ''').fetchall()
    total_vote = conn.execute('''
    SELECT count(*) AS total_vote_10_min
    FROM vote
    WHERE created_at > datetime('now','-10 minute')
    ''').fetchall()
    conn.close()
    vote_by_cand = []
    for cand in count_vote:
        vote_by_cand.append({k: cand[k] for k in cand.keys()})

    total_vote_10_min = []
    for total in total_vote:
        total_vote_10_min.append({k: total[k] for k in total.keys()})

    return jsonify(vote_by_cand, total_vote_10_min)


@app.route('/vote/', methods=["POST"])
def vote():
    if 'candidate_id' not in request.json:
        return json.dumps({'success': False, "error_message": "candidate_id is required!"}), 400, {'ContentType': 'application/json'}
            # "candidate_id is required!", 400

    else:
        conn = db_connection()
        candidate_id = request.json['candidate_id']
        if 'opinion' in request.json:
            opinion = request.json['opinion']
            conn.execute('INSERT INTO vote (candidate_id, opinion) VALUES (?, ?)',
                         (candidate_id, opinion))
        else:
            conn.execute('INSERT INTO vote (candidate_id) VALUES (?)',
                         (candidate_id,))
    conn.commit()
    conn.close()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
