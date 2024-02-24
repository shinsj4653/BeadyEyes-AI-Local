# Import the InferencePipeline object
from inference import InferencePipeline
# Import the built in render_boxes sink for visualizing results
from inference.core.interfaces.stream.sinks import render_boxes


import os

# 환경 변수 설정
os.environ["ROBOFLOW_API_KEY"] = "xD1MfAWZdjVq5pJBV6Av"

# initialize a pipeline object
pipeline = InferencePipeline.init(
    model_id="yolov8x-1280", # Roboflow model to use
    video_reference="https://storage.googleapis.com/com-roboflow-marketing/inference/people-walking.mp4", # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    on_prediction=render_boxes, # Function to run after each prediction
)
pipeline.start()
pipeline.join()
