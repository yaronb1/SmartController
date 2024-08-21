import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

from definitions.config import ROOTDIR

model_path = os.path.join(ROOTDIR, 'models', 'gesture_recognizer.task')
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


# Create a gesture recognizer instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print('gesture recognition result: {}'.format(result))


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
# with GestureRecognizer.create_from_options(options) as recognizer:
#     # The detector is initialized. Use it here.
#     # ...
#     print('running')


if __name__=='__main__':

    import cv2


    cap = cv2.VideoCapture(0)

    #with GestureRecognizer.create_from_options(options) as recognizer:
    recognizer = GestureRecognizer.create_from_options(options)
    while True:

        success,img =  cap.read()
        if success:
            ts = cap.get(cv2.CAP_PROP_POS_MSEC)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
            recognizer.recognize_async(mp_image, int(ts))



        cv2.imshow('org', img)
        if cv2.waitKey(1) and 0xFF==ord('q'):
            break

