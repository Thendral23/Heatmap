import torch

class Model:

    def __init__(self):
        try:
            # Load the YOLOv5 model(Pretrained)
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)
        except Exception as exception:
            print("Constructor method failed while loading the model", exception.args)
