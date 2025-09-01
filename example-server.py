# from flask import Flask, jsonify, request #!, requests
# from flask_cors import CORS
# import json
# import requests
# import os
# from Xor_2 import xor_on_key

# app = Flask(__name__)
# CORS(app)

# my_file = r"C:\my_python\kodcod1\saveData.json"


# def filtering_date(from_year, from_month, from_day, to_year, to_month, to_day):
#     result = {}
#     if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
#             my_dict = [{}]
#     else:
#         with open(my_file, 'r', encoding='utf-8') as file:
#             try:
#                 my_dict = json.load(file)
#             except json.JSONDecodeError:
#                 my_dict = [{}]

#     if my_dict[0]:
#         for year in my_dict[0]:
#             if int(year) >= int(from_year) and int(year) <= int(to_year):
#                 for month in my_dict[0][year]:
#                     if int(month) >= int(from_month) and int(month) <= int(to_month):
#                         for day in my_dict[0][year][month]:
#                             if int(day) >= int(from_day) and int(day) <= int(to_day):
#                                 result[day] = my_dict[0][year][month][day]
    
#     return jsonify(result)


# @app.route('/save_data', methods=['POST'])
# def save_data():
#     """
#     Get data from agent and save it per a minute in json file
#     """
#     data = request.get_json()
#     print(data)

#     if not data:
#         return {"status": "empty"}

#     if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
#         my_dict = [{}]
#     else:
#         with open(my_file, 'r', encoding='utf-8') as file:
#             try:
#                 my_dict = json.load(file)
#             except json.JSONDecodeError:
#                 my_dict = [{}]

#     for year in data[0]:
#         if year in my_dict[0]:
#             for month in data[0][year]:
#                 if month in my_dict[0][year]:
#                     for day in data[0][year][month]:
#                         if day in my_dict[0][year][month]:
#                             for time in data[0][year][month][day]:
#                                 if time in my_dict[0][year][month][day]:
#                                     my_dict[0][year][month][day][time] += xor_on_key(data[0][year][month][day][time], 7)
#                                 else:
#                                     my_dict[0][year][month][day][time] = xor_on_key(data[0][year][month][day][time], 7)
#                         else:
#                             my_dict[0][year][month][day] = data[0][year][month][day]
#                 else:
#                     my_dict[0][year][month] = data[0][year][month]
#         else:
#             my_dict[0][year] = data[0][year]

#     with open(my_file, 'w', encoding='utf-8') as updated_file:
#         json.dump(my_dict, updated_file, ensure_ascii=False)

#     print(my_dict)
#     return jsonify({"status": True})


# @app.route('/', methods=['GET'])
# def get_full_data():
#     """
#     function allows to intelligence person see all the data from the json  file
#     """
#     if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
#             my_dict = [{}]
#     else:
#         with open(my_file, 'r', encoding='utf-8') as file:
#             try:
#                 my_dict = json.load(file)
#             except json.JSONDecodeError:
#                 my_dict = [{}]
#     return jsonify(my_dict)


# @app.route('/filter/date', methods=['POST'])
# def filter_by_date():
#     """
#     function to filter the data by months and/or days.
#     the function should recive information in the following format:
#     body : { from_year : "2025", from_month : "05", from_day : "18", to_year : "2025", to_month : "08", to_day : "26" }
#     """
#     date = request.get_json()
#     from_year = date.get('from_year')
#     from_month = date.get('from_month')
#     from_day = date.get('from_day')
#     # to_year = date.get('year')
#     # to_month = date.get('month')
#     # to_day = date.get('day')
#     to_year = date.get('to_year')      # תיקון כאן!
#     to_month = date.get('to_month')    # תיקון כאן!
#     to_day = date.get('to_day')        # תיקון כאן!
#     return filtering_date(from_year, from_month, from_day, to_year, to_month, to_day)




# @app.route('/filter/string', methods=['POST'])
# def filter_by_string():
#     """
#     function to filter the data by specified word.
#     the function should recive information in the following format: body : { word : "some_string" } 
#     -- without speaces!
#     """
#     string = request.get_json()
#     word = string.get('word')
#     result = ''

#     if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
#             my_dict = [{}]
#     else:
#         with open(my_file, 'r', encoding='utf-8') as file:
#             try:
#                 my_dict = json.load(file)
#             except json.JSONDecodeError:
#                 my_dict = [{}]
#     if my_dict[0]:
#         for year in my_dict[0]:
#             for month in my_dict[0][year]:
#                 for day in my_dict[0][year][month]:
#                     for time in my_dict[0][year][month][day]:
#                         if word in time:
#                             result = my_dict[0][year][month][day]
    
#     return jsonify(result)


# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from Xor_2 import xor_on_key

app = Flask(__name__)
CORS(app)

my_file = r"C:\my_python\kodcod1\saveData.json"


def safe_load_json():
    """טעינה בטוחה של קובץ JSON"""
    try:
        if not os.path.exists(my_file) or os.stat(my_file).st_size == 0:
            return [{}]
        
        with open(my_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if isinstance(data, list) else [{}]
            
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return [{}]


def convert_to_simple_format(data):
    """המרת הנתונים לפורמט פשוט: תאריך:טקסט"""
    result = []
    
    if not data or not isinstance(data, list) or len(data) == 0 or not data[0]:
        return result
    
    # עובר על השנים
    for year in data[0]:
        # עובר על החודשים
        for month in data[0][year]:
            # עובר על הימים
            for day in data[0][year][month]:
                times_data = data[0][year][month][day]
                
                # יוצר אובייקט חדש לכל יום
                day_object = {}
                
                # עובר על הזמנים ביום
                for time in times_data:
                    content = times_data[time]
                    
                    # יוצר מפתח בפורמט: DD/MM/YY HH:MM
                    formatted_date = f"{day.zfill(2)}/{month.zfill(2)}/{year} {time}"
                    day_object[formatted_date] = content
                
                # אם יש נתונים ביום הזה, מוסיף לתוצאה
                if day_object:
                    result.append(day_object)
    
    return result


def safe_save_json(data):
    """שמירה בטוחה של קובץ JSON"""
    try:
        os.makedirs(os.path.dirname(my_file), exist_ok=True)
        
        with open(my_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False


def is_date_in_range(year, month, day, from_year, from_month, from_day, to_year, to_month, to_day):
    """בדיקה בטוחה אם תאריך נמצא בטווח"""
    try:
        def safe_int(value, default=1):
            try:
                return int(value) if value else default
            except (ValueError, TypeError):
                return default
        
        # המרה בטוחה למספרים
        y, m, d = safe_int(year), safe_int(month), safe_int(day)
        fy, fm, fd = safe_int(from_year), safe_int(from_month), safe_int(from_day)
        ty, tm, td = safe_int(to_year), safe_int(to_month), safe_int(to_day)
        
        current_date = datetime(y, m, d)
        from_date = datetime(fy, fm, fd)
        to_date = datetime(ty, tm, td)
        
        return from_date <= current_date <= to_date
    except Exception as e:
        print(f"Date range error: {e}")
        return False


def filtering_date(from_year, from_month, from_day, to_year, to_month, to_day):
    """פילטור נתונים לפי טווח תאריכים - מחזיר פורמט פשוט"""
    try:
        # בדיקה שכל הפרמטרים קיימים
        if not all([from_year, from_month, from_day, to_year, to_month, to_day]):
            return jsonify({"error": "Missing date parameters"})
        
        data = safe_load_json()
        
        if not data or not data[0]:
            return jsonify([])
        
        result = []
        
        # עובר על השנים
        for year in data[0]:
            # עובר על החודשים
            for month in data[0][year]:
                # עובר על הימים
                for day in data[0][year][month]:
                    if is_date_in_range(year, month, day, from_year, from_month, from_day, to_year, to_month, to_day):
                        times_data = data[0][year][month][day]
                        
                        # יוצר אובייקט חדש לכל יום מפולטר
                        day_object = {}
                        
                        for time in times_data:
                            content = times_data[time]
                            formatted_date = f"{day.zfill(2)}/{month.zfill(2)}/{year} {time}"
                            day_object[formatted_date] = content
                        
                        if day_object:
                            result.append(day_object)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Filtering error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/save_data', methods=['POST'])
def save_data():
    """שמירת נתונים - גרסה בטוחה"""
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list) or not data[0]:
            return jsonify({"status": "empty data"})

        my_dict = safe_load_json()
        
        # ודא שהמבנה קיים
        if not my_dict[0]:
            my_dict[0] = {}

        # עיבוד הנתונים בצורה בטוחה
        for year in data[0]:
            if year not in my_dict[0]:
                my_dict[0][year] = {}
            
            for month in data[0][year]:
                if month not in my_dict[0][year]:
                    my_dict[0][year][month] = {}
                
                for day in data[0][year][month]:
                    if day not in my_dict[0][year][month]:
                        my_dict[0][year][month][day] = {}
                    
                    for time in data[0][year][month][day]:
                        try:
                            # עיבוד בטוח של הנתונים
                            new_data = data[0][year][month][day][time]
                            processed_data = xor_on_key(new_data, 7)
                            
                            if time in my_dict[0][year][month][day]:
                                # שילוב הנתונים הקיימים עם החדשים
                                existing = my_dict[0][year][month][day][time]
                                my_dict[0][year][month][day][time] = existing + processed_data
                            else:
                                my_dict[0][year][month][day][time] = processed_data
                                
                        except Exception as e:
                            print(f"Error processing time {time}: {e}")
                            continue

        # שמירה בטוחה
        if safe_save_json(my_dict):
            return jsonify({"status": True})
        else:
            return jsonify({"status": False, "error": "Failed to save"}), 500
            
    except Exception as e:
        print(f"Save data error: {e}")
        return jsonify({"status": False, "error": str(e)}), 500


@app.route('/', methods=['GET'])
def get_full_data():
    """קבלת כל הנתונים - מחזיר פורמט פשוט"""
    try:
        data = safe_load_json()
        simple_format = convert_to_simple_format(data)
        return jsonify(simple_format)
    except Exception as e:
        print(f"Get data error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/filter/date', methods=['POST'])
def filter_by_date():
    """פילטור לפי תאריך - מחזיר פורמט פשוט"""
    try:
        date_params = request.get_json()
        
        if not date_params:
            return jsonify({"error": "No data provided"}), 400
        
        start_date = date_params.get('start_date')
        end_date = date_params.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({"error": "Both start_date and end_date are required"}), 400
        
        # Parse start_date (DD-MM-YYYY format)
        start_parts = start_date.split('-')
        from_day = start_parts[0]
        from_month = start_parts[1] 
        from_year = start_parts[2]
        
        # Parse end_date (DD-MM-YYYY format)  
        end_parts = end_date.split('-')
        to_day = end_parts[0]
        to_month = end_parts[1]
        to_year = end_parts[2]
        
        return filtering_date(from_year, from_month, from_day, to_year, to_month, to_day)
        
    except Exception as e:
        print(f"Filter by date error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/filter/string', methods=['POST'])
def filter_by_string():
    """פילטור לפי מחרוזת - מחזיר פורמט פשוט"""
    try:
        string_params = request.get_json()
        
        if not string_params:
            return jsonify({"error": "No data provided"}), 400
            
        word = string_params.get('word')
        
        if not word:
            return jsonify({"error": "No word provided"}), 400

        data = safe_load_json()
        result = []
        
        if data[0]:
            day_object = {}
            
            # עובר על השנים
            for year in data[0]:
                # עובר על החודשים
                for month in data[0][year]:
                    # עובר על הימים
                    for day in data[0][year][month]:
                        times_data = data[0][year][month][day]
                        
                        # עובר על הזמנים
                        for time in times_data:
                            content = times_data[time]
                            
                            # חיפוש המילה בזמן או בתוכן
                            if word.lower() in str(time).lower() or word.lower() in str(content).lower():
                                formatted_date = f"{day.zfill(2)}/{month.zfill(2)}/{year} {time}"
                                day_object[formatted_date] = content
            
            if day_object:
                result.append(day_object)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Filter by string error: {e}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(500)
def handle_internal_error(e):
    print(f"Internal error: {e}")
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def handle_not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == '__main__':
    try:
        # יצירת תיקיית היעד
        os.makedirs(os.path.dirname(my_file), exist_ok=True)
        
        print("Starting Flask server...")
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except Exception as e:
        print(f"Failed to start server: {e}")