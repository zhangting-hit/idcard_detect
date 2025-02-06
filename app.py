from flask import Flask, request, jsonify
from PIL import Image, ExifTags
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
    print(image.size)
    # 如果图片被旋转了，手动旋转回来
    if image.mode != 'RGB':
        image = image.convert('RGB')  # 确保是RGB模式

    if hasattr(image, '_getexif'):  # 检查是否有Exif信息
        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(0x0112)
            if orientation == 3:
                image = image.transpose(Image.ROTATE_180)
            elif orientation == 6:
                image = image.transpose(Image.ROTATE_270)
            elif orientation == 8:
                image = image.transpose(Image.ROTATE_90)
    # 使用YOLO模型进行目标检测
    detected, score, bbox = yolo.detect_image_flask(image)

    if bbox is not None:
        top, bottom, left, right = bbox
        result = {
            'id_card': detected,
            'score' : float(score),
            'bbox': {
                'top': int(top),
                'bottom': int(bottom),
                'left': int(left),
                'right': int(right)
            },
                       
        }
    else:
        result = {
            'id_card': detected,
            'bbox': None,
            'score': None
        }

    return jsonify(result)

if __name__ == '__main__':
    # 运行Flask应用，指定端口为4998
    server = pywsgi.WSGIServer(('0.0.0.0', 4998), app)
    server.serve_forever()

