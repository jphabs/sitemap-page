import os
import logging
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get GitHub token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GitHub token is not set. Please add it to the .env file.")

# GitHub API URL for triggering workflow
GITHUB_API_URL = 'https://api.github.com/repos/jphabs/sitemap-page/dispatches'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-sitemap', methods=['POST'])
def generate_sitemap():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        payload = {
            'event_type': 'sitemap-generation',
            'client_payload': {'url': url}
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GITHUB_TOKEN}'
        }

        # Log request details (with token hidden)
        logging.debug("Sending request to GitHub API: %s", GITHUB_API_URL)
        logging.debug("Payload: %s", payload)
        logging.debug("Headers: Content-Type: application/json, Authorization: Bearer [HIDDEN]")

        # Send the POST request to GitHub API
        response = requests.post(GITHUB_API_URL, json=payload, headers=headers)

        # Log the response
        logging.debug("GitHub Response Status Code: %d", response.status_code)
        logging.debug("GitHub Response Text: %s", response.text)

        if response.status_code == 201:
            return jsonify({'message': f'Sitemap generation started for {url}'}), 200
        elif response.status_code == 204:
            # Handle GitHub's No Content response gracefully
            return jsonify({'message': 'No Content: The request was accepted, but no action was triggered. Please verify the GitHub Action configuration.'}), 204
        else:
            error_message = response.json().get('message', 'Unknown error')
            return jsonify({'error': f'Failed to trigger GitHub Action: {error_message}'}), response.status_code

    except requests.exceptions.RequestException as e:
        logging.error("Request exception: %s", str(e))
        return jsonify({'error': f'Request error: {str(e)}'}), 500
    except Exception as e:
        logging.error("General exception: %s", str(e))
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)