import cv2 # type: ignore
from cvzone.HandTrackingModule import HandDetector # type: ignore
import numpy as np # type: ignore
import tensorflow as tf # type: ignore
import time
import paho.mqtt.client as mqtt # type: ignore

# إعداد الكاميرا
video = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)
run_object_detector = False

# تحميل نموذج TensorFlow Lite
interpreter = tf.lite.Interpreter(model_path="converted_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# MQTT إعداد
broker_address = "broker.hivemq.com"
client = mqtt.Client("client-Id")
client.connect(broker_address, 1883)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/leds/pi")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

# متغيرات تتبع الإجراء الحالي
last_action_sent = ""
action = ""

while True:
    success, frame = video.read()
    if not success:
        print("فشل في التقاط الصورة من الكاميرا.")
        break

    hands, handsType, img = detector.findHands(frame)
    f_type = [[], []]

    if hands:
        if len(hands) == 2:
            f_type[0] = detector.fingersUp(hands[0])
            f_type[1] = detector.fingersUp(hands[1])
        else:
            lmList = hands[0]
            handType = handsType[0]
            fingerUp = detector.fingersUp(lmList)
            if handType == "Right":
                f_type[0] = fingerUp
            else:
                f_type[1] = fingerUp

    if f_type == [[0, 1, 0, 0, 0], [0, 1, 0, 0, 0]]:
        action = "forward"
        run_object_detector = True
    elif f_type == [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0]]:
        action = "right"
    elif f_type == [[0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]:
        action = "left"
    elif f_type == [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]:
        action = "stop"
        run_object_detector = False

    if action and action != last_action_sent:
        client.publish("/leds", action)
        print("تم إرسال:", action)
        last_action_sent = action
        action = ""

    if run_object_detector:
        image_resized = cv2.resize(frame, (320, 320))
        image_np = np.expand_dims(image_resized, axis=0).astype(np.uint8)
        interpreter.set_tensor(input_details[0]['index'], image_np)
        interpreter.invoke()

        boxes = interpreter.get_tensor(output_details[0]['index'])[0]
        class_ids = interpreter.get_tensor(output_details[1]['index'])[0]
        scores = interpreter.get_tensor(output_details[2]['index'])[0]

        height, width, _ = frame.shape

        for i in range(len(scores)):
            if scores[i] > 0.5:
                ymin, xmin, ymax, xmax = boxes[i]
                (left, right, top, bottom) = (int(xmin * width), int(xmax * width),
                                              int(ymin * height), int(ymax * height))
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                label = f"{int(class_ids[i])}: {scores[i]:.2f}"
                cv2.putText(frame, label, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("object detector", frame)
    else:
        if cv2.getWindowProperty("object detector", cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow("object detector")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.01)

video.release()
cv2.destroyAllWindows()
