import json

# 保存检测结果到文件
def save_results(results, output_file="results.json"):
    with open(output_file, "w") as f:
        json.dump(results, f)

# 读取历史检测结果
def load_previous_results(input_file="results.json"):
    try:
        with open(input_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# Change Detection 功能：对比当前与历史检测结果
def change_detection(current_results, previous_results):
    if not previous_results:
        print("No previous results found. This is the first detection.")
        return
    print("Comparing current results with previous results...")
    current_objects = len(current_results["name"])
    previous_objects = len(previous_results["name"])
    print(f"Previous Objects: {previous_objects}, Current Objects: {current_objects}")
    if current_objects != previous_objects:
        print("Change Detected: Object count changed.")
    else:
        print("No change detected.")
