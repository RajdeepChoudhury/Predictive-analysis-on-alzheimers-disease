from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def diagnose_alzheimer(mmse, adl):
    return mmse <= 24 and adl <= 5


@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.get_json()

    # Check if request body exists
    if not data:
        return jsonify({'error': 'No data received'}), 400

    required_fields = [
        'patient_id', 'age', 'systolic_bp', 'cholesterol_ldl',
        'mmse', 'functional_assessment', 'adl'
    ]

    # Check for missing fields
    for field in required_fields:
        if field not in data or data[field] == '':
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        patient_id = str(data['patient_id'])
        age = int(data['age'])
        systolic_bp = int(data['systolic_bp'])
        cholesterol_ldl = float(data['cholesterol_ldl'])
        mmse = int(data['mmse'])
        functional_assessment = float(data['functional_assessment'])
        adl = int(data['adl'])
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400

    # Validation checks
    if not (0 <= mmse <= 30):
        return jsonify({'error': 'MMSE must be between 0 and 30'}), 400

    if not (0 <= adl <= 10):
        return jsonify({'error': 'ADL must be between 0 and 10'}), 400

    if age <= 0 or age > 130:
        return jsonify({'error': 'Age must be between 1 and 130'}), 400

    if systolic_bp <= 0:
        return jsonify({'error': 'Systolic BP must be a positive number'}), 400

    # Diagnosis logic
    has_alzheimer = diagnose_alzheimer(mmse, adl)

    # Risk level classification
    if mmse <= 17:
        risk_level = 'Severe'
    elif mmse <= 23:
        risk_level = 'Moderate'
    elif mmse <= 27:
        risk_level = 'Mild'
    else:
        risk_level = 'Normal'

    # Response
    result = {
        'patient_id': patient_id,
        'age': age,
        'systolic_bp': systolic_bp,
        'cholesterol_ldl': cholesterol_ldl,
        'mmse': mmse,
        'functional_assessment': functional_assessment,
        'adl': adl,
        'diagnosis': "Alzheimer's Disease Detected" if has_alzheimer else "No Alzheimer's Disease Detected",
        'has_alzheimer': has_alzheimer,
        'risk_level': risk_level,
        'criteria_met': {
            'mmse_flag': mmse <= 24,
            'adl_flag': adl <= 5
        }
    }

    return jsonify(result), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Server is running'}), 200


if __name__ == '__main__':
    print("Alzheimer's Diagnosis Server running on http://localhost:5000")
    app.run(debug=True, port=5000)