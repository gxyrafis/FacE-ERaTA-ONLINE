from datetime import datetime

class Attempts:
    id = -1
    result = False
    percentage = 0.0
    emotion_detected = ""
    target_emotion = ""
    img = ""
    date = datetime.now()

    def __init__(self, id, result, percentage, emotion_detected, target_emotion, img, date):
        if id is not None:
            self.id = id
        else:
            self.id = None
        if result is not None:
            self.result = result
        else:
            self.result = None
        self.percentage = percentage
        self.emotion_detected = emotion_detected
        if target_emotion is not None:
            self.target_emotion = target_emotion
        else:
            self.target_emotion = None
        self.img = img
        self.date = date