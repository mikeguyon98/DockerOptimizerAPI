import subprocess
import json
import re




#find alternative to stderr for docker functions

def delete_docker_image(image_name):
    # Delete the Docker image using the Docker CLI
    print(f"Deleting Docker image: {image_name}")
    command = f"docker rmi {image_name}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        print("Error in deleting Docker image:")
        print(stderr.decode())
        return False
    return True

def pull_docker_image(image_url):
    # Pull the Docker image using the Docker CLI
    print(f"Pulling Docker image: {image_url}")
    command = f"docker pull {image_url}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stderr.decode())
    print("Success")
    # if stderr:
    #     print("Error in pulling Docker image:")
    #     print(stderr.decode())
    #     return False
    return True

def analyze_docker_image(image_name):
    # Run Dive in non-interactive mode
    print("Running Dive")
    result = subprocess.run(['dive', image_name, '--ci'], capture_output=True, text=True)
    output = result.stdout
    print("Process Ran")

    if result.returncode != 0:
        print("Error running Dive:", result.stderr)
        return
    stats = parse_dive_output(output)
    return {
        'image_name': image_name,
        'stats': stats,
        'output': output
    }

def parse_dive_output(output):
    # Regular expressions to capture the required values
    efficiency_pattern = r'efficiency:\s*([\d.]+)\s*%'
    wasted_bytes_pattern = r'wastedBytes:\s*(\d+)\s*bytes'
    user_wasted_percent_pattern = r'userWastedPercent:\s*([\d.]+)\s*%'
    
    # Search for the patterns in the output
    efficiency_match = re.search(efficiency_pattern, output)
    wasted_bytes_match = re.search(wasted_bytes_pattern, output)
    user_wasted_percent_match = re.search(user_wasted_percent_pattern, output)
    
    # Extract the values and convert them to the appropriate types
    efficiency = float(efficiency_match.group(1)) if efficiency_match else None
    wasted_bytes = int(wasted_bytes_match.group(1)) if wasted_bytes_match else None
    user_wasted_percent = float(user_wasted_percent_match.group(1)) if user_wasted_percent_match else None

    # Construct the dictionary
    result = {
        'efficiency': efficiency,
        'wastedBytes': wasted_bytes,
        'userWastedPercent': user_wasted_percent
    }

    return result
    
if __name__ == "__main__":
    image_name = "mikeguyon98/iprecorder"
    analyze_docker_image(image_name)
    # analysis_result = analyze_docker_image(image_name)
    # if analysis_result:
    #     print(json.dumps(analysis_result, indent=4))