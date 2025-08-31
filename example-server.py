from flask import Flask, jsonify, request #!, requests
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app)

@app.route('/save_data', methods=['POST'])
def get_data():
    data = request.json
    print(data)
    return [{"status":True}]



if __name__ == '__main__':
    app.run(debug=True)
