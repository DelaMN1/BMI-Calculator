from flask import Flask, app, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)


def get_bmi(weight, height, unit='metric'):
    if unit == 'metric':
        bmi = weight / (height ** 2)
    elif unit == 'imperial':
        bmi = 703 * (weight / (height ** 2))
    else:
        raise ValueError("Invalid unit. Use metric or imperial")

    return bmi

def classify_bmi(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi <= 24.9:
        return 'Normal'
    elif 25 <= bmi <= 29.5:
        return 'Overweight'
    else:
        return 'Obese'
    

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    
    try:
        weight = float(data['weight'])
        height = float(data['height'])
        unit = data.get('unit', 'metric').lower()

        bmi = get_bmi(weight, height, unit)
        status = classify_bmi(bmi)

        return jsonify({
            'bmi': round(bmi, 2),
            'status': status
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)