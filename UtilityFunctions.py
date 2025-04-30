import urllib

import cv2
import numpy as np
import pandas as pd
from cv2 import VideoCapture
from deepface import DeepFace
import plotly.express as px


def emotionWordSwitch(emotion):
    if emotion == "Anger":
        return "angry"
    elif emotion == "Sadness":
        return "sad"
    elif emotion == "Disgust":
        return "disgust"
    elif emotion == "Fear":
        return "fear"
    elif emotion == "Happiness":
        return "happy"
    elif emotion == "Surprise":
        return "surprise"
    elif emotion == "Neutral":
        return "neutral"


def emotionWordSwitchR(emotion):
    if emotion == "angry":
        return "Anger"
    elif emotion == "sad":
        return "Sadness"
    elif emotion == "disgust":
        return "Disgust"
    elif emotion == "fear":
        return "Fear"
    elif emotion == "happy":
        return "Happiness"
    elif emotion == "surprise":
        return "Surprise"
    elif emotion == "neutral":
        return "Neutral"

def emotionAnalysis(picture, emotion, retinaface):
    mode = "opencv"
    if retinaface == True:
        mode = "retinaface"
    emotion_analysis = DeepFace.analyze(
        img_path=picture,
        actions=['emotion'],
        detector_backend=mode,
    )
    if emotion == "T":
        emotion = emotion_analysis[0]["dominant_emotion"]
    else:
        emotion = emotionWordSwitch(emotion)
    accuracy = emotion_analysis[0]["emotion"][emotion]
    #fig = makeStarChart(emotion_analysis[0])
    if emotion_analysis[0]["dominant_emotion"] == emotion:
        return ["Success" , accuracy, emotionWordSwitchR(emotion_analysis[0]["dominant_emotion"]), emotion_analysis[0]["emotion"]]
    else:
        return ["Failure", accuracy, emotionWordSwitchR(emotion_analysis[0]["dominant_emotion"]), emotion_analysis[0]["emotion"]]

def checkCamValidity(source):
    cam = VideoCapture(source)
    if cam is None or not cam.isOpened():
        cam.release()
        return False
    cam.release()
    return True

def makeStarChart(emotion_analysis):
    anger_percentage = emotion_analysis["emotion"]["angry"]
    sadness_percentage = emotion_analysis["emotion"]["sad"]
    disgust_percentage = emotion_analysis["emotion"]["disgust"]
    fear_percentage = emotion_analysis["emotion"]["fear"]
    happiness_percentage = emotion_analysis["emotion"]["happy"]
    surprise_percentage = emotion_analysis["emotion"]["surprise"]
    neutral_percentage = emotion_analysis["emotion"]["neutral"]

    df = pd.DataFrame(dict(
        r = [happiness_percentage, anger_percentage, sadness_percentage, fear_percentage, surprise_percentage, disgust_percentage, neutral_percentage],
        theta= ["Happiness", "Anger", "Sadness", "Fear", "Surprise", "Disgust", "Neutral"]
    ))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')
    return fig
