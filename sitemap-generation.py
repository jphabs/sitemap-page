import os
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get the GitHub token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GitHub token is not set. Please add it to the .env file.")

# GitHub API endpoint for dispatching the workflow
GITHUB_API_URL = 'https://api.github.com/repos/jphabs/sitemap-page/dispatches'

# Endpoint to trigger the sitemap generation
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to trigger the sitemap generation process
@app.route('/generate-sitemap', methods=['POST'])
def generate_sitemap():
    data = request.json

    # Validate input URL
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # Prepare the payload for GitHub Actions
        payload = {
            'event_type': 'sitemap-generation',
            'client_payload': {'url': url}
        }

        # Make the request to GitHub to trigger the action
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GITHUB_TOKEN}'
        }

        response = requests.post(GITHUB_API_URL, json=payload, headers=headers)

        if response.status_code == 201:
            return jsonify({'message': f'Sitemap generation started for {url}'}), 200
        else:
            return jsonify({'error': 'Failed to trigger GitHub Action'}), response.status_code

    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)