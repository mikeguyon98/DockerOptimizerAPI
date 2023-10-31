import subprocess
import json
import sys

def pull_docker_image(image_url):
    # Pull the Docker image using the Docker CLI
    print(f"Pulling Docker image: {image_url}")
    command = f"docker pull {image_url}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        print("Error in pulling Docker image:")
        print(stderr.decode())
        return False
    return True

def analyze_docker_image(image_url):
    # Pull the Docker image first
    if not pull_docker_image(image_url):
        return None

    # Run Dive and capture its JSON output
    command = f"dive {image_url} --json"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        print("Error in running Dive:")
        print(stderr.decode())
        return None

    # Parse JSON output
    try:
        dive_output = json.loads(stdout)
    except json.JSONDecodeError:
        print("Failed to parse Dive's output.")
        return None

    # Extract relevant information
    inefficiencies = dive_output.get('inEfficientFiles', [])
    layer_details = dive_output.get('layers', [])

    results = {
        "image_url": image_url,
        "total_inEfficient_files": len(inefficiencies),
        "inefficient_files": inefficiencies,
        "layers": layer_details
    }

    return results

def format_for_llm(results):
    formatted_text = f"Docker Image Analysis Report for {results['image_url']}:\n"
    formatted_text += f"Total Inefficient Files: {results['total_inEfficient_files']}\n"
    formatted_text += "Inefficient Files:\n"

    for file in results['inefficient_files']:
        formatted_text += f" - {file['name']} (Size: {file['size']})\n"

    formatted_text += "Layers Details:\n"
    for layer in results['layers']:
        formatted_text += f" - ID: {layer['id']} (Size: {layer['size']} bytes)\n"

    return formatted_text

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_docker_image.py <docker_image_url>")
        sys.exit(1)

    image_url = sys.argv[1]  # Get the Docker image URL from command line arguments
    analysis_results = analyze_docker_image(image_url)
    if analysis_results:
        formatted_output = format_for_llm(analysis_results)
        print(formatted_output)
        # Now, you can feed `formatted_output` into an LLM for further processing or explanation generation.
