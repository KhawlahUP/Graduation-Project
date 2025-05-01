import tensorflow as tf
import cv2
import numpy as np
import threading
import pyttsx3
WIDTH = 640
HEIGHT = 480

class DetectorThread(threading.Thread):
    def __init__(self, model_path, labels, threshold=0.4):
        threading.Thread.__init__(self)
        self.interpreter = tf.lite.Interpreter(model_path = model_path)
        self.interpreter.allocate_tensors()
        self.labels = self.load_labels(labels)
        self.threshold = threshold

    def load_labels(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return {i: line.strip() for i, line in enumerate(f.readlines())}
    
    def set_input_tensor(self, image):
        tensor_index = self.interpreter.get_input_details()[0]['index']
        input_tensor = self.interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def get_output_tensor(self, index):
        output_details = self.interpreter.get_output_details()[index]
        tensor = np.squeeze(self.interpreter.get_tensor(output_details['index']))
        return tensor

    def start_detector(self, frame):
        img = frame
        img = cv2.resize(img, (320, 320))
        self.set_input_tensor(img)
        self.interpreter.invoke()
        boxes = self.get_output_tensor(0)
        classes = self.get_output_tensor(1)
        scores = self.get_output_tensor(2)
        count = int(self.get_output_tensor(3))
        results = []
        for i in range(count):
            if scores[i] >= self.threshold:
                result = {
                    'bbox': boxes[i],
                    'clsID': classes[i],
                    'score': scores[i]
                }
                results.append(result)
        return results

    def draw_results(self, img, results):
        for res in results:
            ymin, xmin, ymax, xmax = res['bbox']
            xmin = int(xmin * WIDTH)
            xmax = int(xmax * WIDTH)
            ymin = int(ymin * HEIGHT)
            ymax = int(ymax * HEIGHT)
            self.recognize_close_objects(res)
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            cv2.putText(img, str(self.labels[res['clsID']]), (xmin+6, ymax-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


    def speak_warning(self,class_name):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say("There is a " + class_name + " close to us.")
        try:
            engine.runAndWait()
        except:
            pass

    def recognize_close_objects(self, obj):
        x1, y1, x2, y2 = obj['bbox']
        boxW, boxH = x2 - x1, y2 - y1        
        is_close = (boxW+boxH)*2 >= 2
        print((boxW+boxH)*2)
        class_name = str(self.labels[obj['clsID']])
        if is_close:
            t = threading.Thread(target=self.speak_warning, args=(class_name,))
            t.start()

    def recognize_objects(self, frame):
        results = self.start_detector(frame)
        self.draw_results(frame, results)