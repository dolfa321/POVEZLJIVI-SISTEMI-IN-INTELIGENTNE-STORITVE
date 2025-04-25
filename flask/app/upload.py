from flask import Blueprint, request, jsonify
import os
import subprocess
import json
from pathlib import Path

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    data = request.form.get('data')
    if not data:
        return jsonify({'error': 'Missing data parameter'}), 400

    try:
        data = json.loads(data)
        mode = data.get('mode')
        if mode not in [1, 2]:
            return jsonify({'error': 'Invalid mode. Use 1 for predefined workouts or 2 for custom input'}), 400

        project_root = Path(__file__).resolve().parents[2]
        python_path = project_root / '.venv' / 'Scripts' / 'python.exe'
        script_path = project_root / 'predictor' / 'scripts' / 'klemen_parser.py'

        args = [str(python_path), str(script_path)]

        if mode == 1:
            args.extend(['--choice', '1'])
        elif mode == 2:
            workout_data = data.get('workout_data')
            if not workout_data:
                return jsonify({'error': 'Missing workout_data for mode 2'}), 400
            args.extend(['--choice', '2', '--workout', json.dumps(workout_data)])

        if not os.path.exists(str(python_path)):
            return jsonify({'error': 'Python executable not found', 'path': str(python_path)}), 500

        if not os.path.exists(str(script_path)):
            return jsonify({'error': 'Script not found', 'path': str(script_path)}), 500

        result = subprocess.run(args, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': 'Error running the script', 'details': result.stderr}), 500

        return jsonify({'message': 'File uploaded successfully', 'results': result.stdout}), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the request', 'details': str(e)}), 500