from flask import Flask, request, jsonify
from services.optimizer import analyze_docker_image, format_for_llm

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.json
    image_url = data.get('image_url')
    
    if not image_url:
        return jsonify({"error": "No image_url provided"}), 400

    analysis_results = analyze_docker_image(image_url)
    if analysis_results:
        formatted_output = format_for_llm(analysis_results)
        return jsonify({"analysis": formatted_output})
    else:
        return jsonify({"error": "Failed to analyze the image"}), 500

if __name__ == '__main__':
    app.run(debug=True)
