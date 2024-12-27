import torch
from pathlib import Path

# YOLOv5 模型加载
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory

# 加载预训练的YOLOv5模型
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo=True)


# 自定义函数：进行目标检测
def detect_objects(image_path):
    results = model(image_path)  # 执行检测
    results.print()  # 打印检测结果
    results.save()   # 保存带有检测框的图片
    return results.pandas().xyxy[0].to_dict()  # 返回检测框数据


def run():
    """
    YOLOv5 检测功能: 支持图像、视频、摄像头等输入。
    """
    print("Running YOLOv5 detection...")

    # 示例：输入图像检测
    image_path = "/Users/yuxinyue/Desktop/ROOT/Edge_System/yolov5/data/images/zidane.jpg"  # 替换为你的输入图像路径
    detection_results = detect_objects(image_path)
    print("Detection Results:", detection_results)

    print("Detection Complete!")


if __name__ == "__main__":
    """
    程序入口：执行自定义检测
    """
    run()
