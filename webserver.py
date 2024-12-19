from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/save', methods=['POST'])
def save_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        with open('/home/mrkal/git/sensehat-snake/data.json', 'r+') as f:
            file_data = json.load(f)
            file_data.append(data)
            f.seek(0)
            json.dump(file_data, f)
        return jsonify({"message": "Data appended successfully"}), 200
    except json.JSONDecodeError:
        with open('/home/mrkal/git/sensehat-snake/data.json', 'w') as f:
            json.dump([data], f)
        return jsonify({"message": "Data appended successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get', methods=['GET'])
def get_data():
    try:
        with open('/home/mrkal/git/sensehat-snake/data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)