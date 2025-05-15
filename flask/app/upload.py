import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, base_dir)
from predictor.scripts.classify_user import classify_user
from flask import Blueprint, request, jsonify

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    print("Workout Type from frontend:", request.form.get('workoutType'))
    print()
    print()
    print()
    print()
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        percentile, recommendations = classify_user(file_path, request.form.get('workout_type',
                                                                                request.form.get('workoutType',
                                                                                                 'Strength')),
                                                    request.form.get('age', 25))
        print(percentile, recommendations)
        for f in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return jsonify({
            'message': 'File processed successfully',
            'percentile': percentile,
            'rec': recommendations
        }), 200

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the request', 'details': str(e)}), 500
