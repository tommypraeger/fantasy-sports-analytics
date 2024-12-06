from flask import Flask, jsonify, request
from flask_cors import CORS

from application import handle_league_analysis

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def post_data():
    data = request.json
    response = handle_league_analysis(data)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
