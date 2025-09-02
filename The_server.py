import json, os
from flask import Flask, jsonify, request
from flask_cors import CORS
from Xor_2 import xor_on_key
from datetime import datetime

app = Flask(__name__)
CORS(app)

my_file = r"saveData.json"


@app.route('/save_data', methods=['POST'])
def save_data():
    """
    Get data from agent and save it per a minute in json file
    """
    data = request.get_json()

    if not data:
        return jsonify({"status": "empty"})

    for item in data:
        item["text"] = xor_on_key(item["text"], 7)

    if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
        my_dict = list(data)
    else:
        with open(my_file, 'r', encoding='utf-8') as file:
            try:
                my_dict = json.load(file)
                my_dict.extend(data)
            except json.JSONDecodeError:
                my_dict = []
            except:
                return jsonify({"status": False})

    with open(my_file, 'w', encoding='utf-8') as updated_file:
        json.dump(my_dict, updated_file, ensure_ascii=False)

    return jsonify({"status": True})


@app.route('/', methods=['GET'])
def get_full_data():
    """
    function allows to intelligence person see all the data from the json  file
    """
    if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
            my_dict = []
    else:
        with open(my_file, 'r', encoding='utf-8') as file:
            try:
                my_dict = json.load(file)
            except json.JSONDecodeError:
                my_dict = []
    return jsonify(my_dict)


@app.route('/filter/date', methods=['POST'])
def filter_by_date():
    """
        function to filter the data by months and/or days.
        the function should recive information in the following format:
        body : { from_year : "2025", from_month : "05", from_day : "18", to_year : "2025", to_month : "08", to_day : "26" }
    """
    date = request.get_json()
    from_date_str = f"{date['from_year']}-{date['from_month']}-{date['from_day']}"
    to_date_str = f"{date['to_year']}-{date['to_month']}-{date['to_day']}"

    from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
    to_date = datetime.strptime(to_date_str, "%Y-%m-%d")

    if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
        return jsonify({"status": "empty"})

    with open(my_file, 'r', encoding='utf-8') as file:
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
            continue

    return jsonify(result)




@app.route('/filter/string', methods=['POST'])
def filter_by_string():
    """
    function to filter the data by specified word.
    the function should recive information in the following format: body : { word : "some_string" } 
    -- without speaces!
    """
    string = request.get_json()
    word = string.get('word')
    # t = request.get_json().get('word') # לבדוק אח"כ אם זה יעבוד ככה
    result = []
    if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
        return jsonify({"status": "empty"})
    else:
        with open(my_file, 'r', encoding='utf-8') as file:
            try:
                my_dict = json.load(file)
            except json.JSONDecodeError:
                return jsonify({"status": "error"})
    for item in my_dict:
        if word in item["text"]:
            result.append(item)
    if result:
        return jsonify(result)
    return jsonify({"status": "empty"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)