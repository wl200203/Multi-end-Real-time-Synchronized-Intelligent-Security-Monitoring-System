from detect1 import detect_objects  # Import the object detection function
from change_detection import save_results, load_previous_results, change_detection  # Import Change Detection functions

if __name__ == "__main__":
    # Set the input image path
    image_path = "data/images/bus.jpg"

    # Perform object detection
    print("Running Object Detection...")
    current_results = detect_objects(image_path)
    print("Current Detection Results:", current_results)

    # Load previous detection results
    previous_results = load_previous_results()

    # Save the current detection results
    save_results(current_results, output_file="results.json")
    print("Current results saved to 'results.json'.")

    # Perform Change Detection
    print("\nRunning Change Detection...")
    change_detection(current_results, previous_results)
