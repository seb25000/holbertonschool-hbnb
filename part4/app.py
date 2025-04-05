from flask import Flask, jsonify
from flask_cors import CORS
# ... other imports

app = Flask(__name__)
# Configure CORS to allow requests from any origin (*)
# For production, restrict this to your actual front-end domain
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
# Or, more specifically if running locally with Live Server (default port 5500)
# CORS(app, resources={r"/api/v1/*": {"origins": "http://127.0.0.1:5500"}})

# ... rest of your Flask app setup (Blueprints, etc.)

# Example endpoint adjustment (if not using Blueprints properly)
# Ensure your routes start with /api/v1/ if using the CORS resource pattern above
# For example: @app.route('/api/v1/login', methods=['POST'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=True helps during development
