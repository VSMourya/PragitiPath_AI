import cv2
import mediapipe as mp
from flask import Flask, Response, send_from_directory
from draw_vid import mediapipe_results
import tensorflow as tf
import subprocess, os
from flask_cors import CORS
import multiprocessing
from flask import request
from draw_vid import clear_alert_cache


speech_to_text_process = None
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

def set_gpu_memory_growth():
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    if physical_devices:
        try:
            print("---------------------GPU available")
            for dev in physical_devices:
                tf.config.experimental.set_memory_growth(dev, True)
        except RuntimeError as e:
            print(e)
    else:
        print("--------------Using CPU device")

# set cpu or gpu
set_gpu_memory_growth()

app = Flask(__name__, static_folder='build')
CORS(app)


circles = []  # Declare circles as a global variable


@app.route('/clear_circles', methods=['POST'])
def clear_circles():
    global circles  # Refer to the global variable within the function
    circles.clear()  # Clear the global circles list
    # print("Circles cleared")
    return 'Circles cleared', 200



def gen_frames():

    cap = cv2.VideoCapture(0)
    
    print("====")
    
    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as holistic:
        i = 0

        global circles
        single_frame_alert = False

        color_change, color_num = False, 0
        pen_color = 0
        pen_size = 15
        min_conf = 0.5
        max_hands = 2

        mpHands = mp.solutions.hands
        hands = mpHands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=min_conf,
            min_tracking_confidence=min_conf
        )
        mp_draw = mp.solutions.drawing_utils

        with mpHands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

            while True:
                success, frame = cap.read()  # read the camera frame
                if not success:
                    break
                else:
                    
                    frame, circles, pen_size, pen_color, color_change, color_num, clear_dots  = mediapipe_results(frame, circles, color_change, color_num,
                                                                                            pen_color, pen_size, mpHands, hands,
                                                                                            mp_draw)

                    for position in range(len(circles)):
                        pen_color = circles[position][1]
                        frame = cv2.circle(frame, circles[position][0], pen_size, pen_color, -2)

                    
                    alert_cache = clear_alert_cache()
                    
                    if clear_dots:
                        single_frame_alert = True

                    if single_frame_alert:
                        multi_frame_alert = alert_cache.update_cache(True)
                    else:
                        multi_frame_alert = alert_cache.update_cache(False)


                    if multi_frame_alert:
                        clear_circles()
                        # print("Multiframe_alert ==============>> ",multi_frame_alert)
                        single_frame_alert = False
                        multi_frame_alert = []
                    
                    # Encode the frame in JPEG format
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()

                    # Yield the frame in byte format
                    yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed', defaults={'path': ''})
def serve(path):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/generate_text', methods=['POST'])
def generate_text():
    # Run your Python script here, for example:
    try:
        os.chdir('/Users/vsmourya/Desktop/Personal_projects/SBUHacksVI-Hackathon-Project/server')
        subprocess.run(['python3', 'genAIgcp.py'])
    except:
        print("Error Occured!")
    # Assuming your_script.py writes its output to 'response.txt'
    with open('response.txt', 'r') as file:
        response_text = file.read()
    
    return {'text': response_text}

@app.route('/start_speech_to_text', methods=['POST'])
def start_speech_to_text():
    global speech_to_text_process
    os.chdir('/Users/vsmourya/Desktop/Personal_projects/SBUHacksVI-Hackathon-Project/server')
    if speech_to_text_process is None:
        speech_to_text_process = subprocess.Popen(['python3', 'speech_to_text.py'])
    return {'status': 'started'}

@app.route('/stop_speech_to_text', methods=['POST'])
def stop_speech_to_text():
    global speech_to_text_process
    if speech_to_text_process is not None:
        speech_to_text_process.terminate()
        speech_to_text_process = None
    return {'status': 'stopped'}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
