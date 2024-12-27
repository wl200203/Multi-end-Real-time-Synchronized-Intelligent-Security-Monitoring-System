from flask import Flask, request, jsonify
from detect1 import detect_objects
from change_detection import save_results, load_previous_results, change_detection

app = Flask(__name__)

@app.route("/detect", methods=["POST"])
def detect_api():
    """
    HTTP API 路由：上传图片，执行检测，返回检测结果和Change Detection结果。
    """
    # 接收图片
    file = request.files["image"]
    image_path = "input.jpg"
    file.save(image_path)

    # 执行检测
    current_results = detect_objects(image_path)
    previous_results = load_previous_results()
    save_results(current_results)

    # 执行Change Detection
    change_detection(current_results, previous_results)

    return jsonify({"Detection Results": current_results})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
