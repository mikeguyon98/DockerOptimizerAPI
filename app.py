from dotenv import load_dotenv

from flask import Flask, request, jsonify
from services.optimizer_service import analyze_docker_image

app = Flask(__name__)

load_dotenv()

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.json
    image_name = data.get('image_name')
    print("Image Name: ", image_name)
    if not image_name:
        return jsonify({"error": "No image_name provided"}), 400

    analysis_results = analyze_docker_image(image_name)
    return jsonify(analysis_results)
    # if analysis_results:
    #     formatted_output = format_for_llm(analysis_results)
    #     return jsonify({"analysis": formatted_output})
    # else:
    #     return jsonify({"error": "Failed to analyze the image"}), 500

if __name__ == '__main__':
    app.run(debug=True)
