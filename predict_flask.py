from flask import Flask, request, jsonify
from PIL import Image
from gevent import pywsgi
from yolo import YOLO

app = Flask(__name__)

# 初始化YOLO模型
yolo = YOLO()

@app.route('/predict', methods=['POST'])
def predict():
    # 从请求中获取上传的图片文件
    image_file = request.files['image']

    # 读取图片
    image = Image.open(image_file)

    # 使用YOLO模型进行目标检测
    result = yolo.detect_image_flask(image)

    return jsonify({'result': result})

if __name__ == '__main__':
    # 运行Flask应用，指定端口为4998
    server = pywsgi.WSGIServer(('0.0.0.0', 4998), app)
    server.serve_forever()

