from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

model_id = 'damo/cv_tinynas_object-detection_damoyolo_facemask'
input_location = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/image_detection.jpg'

facemask_detection = pipeline(Tasks.domain_specific_object_detection, model=model_id)
result = facemask_detection(input_location)
print("result is : ", result)