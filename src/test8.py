# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)


@app.route('/process', methods=['POST'])
def process_input():
    input_data = request.json.get('input')
    if input_data:
        url = main(input_data)
        return jsonify({'url': url})
    else:
        return jsonify({'error': 'Input data not provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
