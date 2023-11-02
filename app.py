from dotenv import load_dotenv
import os

import openai
from flask import Flask, request, jsonify

from services.optimizer_service import analyze_docker_image
from services.llm_service import generate_response

app = Flask(__name__)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = "You are a software engineer specializing in Containerization. You are highly skilled in analyzing and improving Docker images using tools such as Dive"

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.json
    try:
        image_name = data.get('image_name')
        dockerfile = data.get('dockerfile')
    except:
        return jsonify({"error": "Invalid JSON"}), 400

    if not image_name:
        return jsonify({"error": "No image_name provided"}), 400

    analysis_results = analyze_docker_image(image_name)
    # turn analysis_results into a string
    # send it to GPT-3
    # return the response from GPT-3
    if analysis_results:
        string_results = str(analysis_results)
        print(string_results)
        response = generate_response(string_results, prompt, dockerfile)
        if response:
            return jsonify({
                "analysis": response,
                "stats": analysis_results['stats']
            })
        else:
            return jsonify({"error": "LLM Failed to analyze image"}), 500
    else:
        return jsonify({"error": "Failed to generate analysis"}), 500


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
