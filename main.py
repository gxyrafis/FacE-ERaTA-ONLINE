import base64
import os
import random
from datetime import datetime

import cv2
import flask
import numpy as np
from flask import Flask, redirect, url_for, render_template, request, jsonify
from PIL import Image
import UtilityFunctions
from UtilityFunctions import emotionAnalysis

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/training", methods=["POST", "GET"])
def training():
    if request.method == "POST":
        uid = datetime.today().strftime("%x").replace('/','-') + datetime.today().strftime("%X").replace(':','-')
        path = None
        picname = None
        pic = flask.request.files['pic']
        if pic.filename == "":
            tmpurl = ""
            try:
                tmpurl = flask.request.values['backendimage'].split(';')[1].split(',')[1]
            except:
                return render_template("training.html", result=None, message=None, picname=None,
                                       success=None,
                                       stats={'happy': 0, 'angry': 0, 'sad': 0, 'fear': 0, 'surprise': 0, 'disgust': 0,
                                              'neutral': 0})
            nparr = np.frombuffer(base64.b64decode(tmpurl), np.uint8)
            pic = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imwrite(os.getcwd() + "/static/" + "livepic" + uid + ".png", pic)
            path = os.getcwd() + "/static/" + "livepic" + uid + ".png"
            picname = "livepic" + uid + ".png"
        else:
            pic.save(os.getcwd() + "/static/" + pic.filename)
            path = os.getcwd() + "/static/" + pic.filename
            picname = pic.filename
        try:
            results = emotionAnalysis(path, "T", False)
        except:
            results = emotionAnalysis(path, "T", True)
        #results[3].write_image("static/starchart" + uid + ".png")
        size = 700, 700
        #chart = Image.open("static/starchart" + uid  + ".png")  # Convert image into 500x500
        #chart.thumbnail(size, Image.Resampling.LANCZOS)
        #chart.save("static/starchart" + uid + ".png")

        im = Image.open(path)
        im.thumbnail(size, Image.Resampling.LANCZOS)
        new_image_path = path
        if ".jpg" in path.lower() or ".jpeg" in path.lower():
            new_image_path = path.replace(".jpg", ".png").replace(".jpeg", ".png").replace(".JPG", ".png").replace(
                ".JPEG", ".png")
            picname = picname.replace(".jpg", ".png").replace(".jpeg", ".png").replace(".JPG", ".png").replace(
                ".JPEG", ".png")
            im.save(new_image_path)
        message = str(round(results[1], 2)) + "%"
        return render_template("training.html",result = results[2], message = message, picname = "/static/" + picname, success = results[0], stats = results[3])
    else:
        return render_template("training.html", result=None, message=None, picname=None,
                                       success=None,
                                       stats={'happy': 0, 'angry': 0, 'sad': 0, 'fear': 0, 'surprise': 0, 'disgust': 0,
                                              'neutral': 0})

@app.route("/random", methods=["POST", "GET"])
def randomemotion():
    if request.method == "POST":
        uid = datetime.today().strftime("%x").replace('/', '-') + datetime.today().strftime("%X").replace(':', '-')
        emotion = request.form.get("emotioninput")
        path = None
        picname = None
        pic = flask.request.files['pic']
        if pic.filename == "":
            tmpurl = ""
            try:
                tmpurl = flask.request.values['backendimage'].split(';')[1].split(',')[1]
            except:
                return render_template("randomemotion.html", emotion=emotion, result=None, message=None, picname=None,
                                       success=None,
                                       stats={'happy': 0, 'angry': 0, 'sad': 0, 'fear': 0, 'surprise': 0, 'disgust': 0,
                                              'neutral': 0})
            nparr = np.frombuffer(base64.b64decode(tmpurl), np.uint8)
            pic = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imwrite(os.getcwd() + "/static/" + "livepic" + uid + ".png", pic)
            path = os.getcwd() + "/static/" + "livepic" + uid + ".png"
            picname = "livepic" + uid + ".png"
        else:
            pic.save(os.getcwd() + "/static/" + pic.filename)
            path = os.getcwd() + "/static/" + pic.filename
            picname = pic.filename
        try:
            results = emotionAnalysis(path, emotion, False)
        except:
            results = emotionAnalysis(path, emotion, True)
        #results[3].write_image("static/starchart" + uid  +".png")
        size = 700, 700
        #chart = Image.open("static/starchart" + uid  + ".png")  # Convert image into 500x500
        #chart.thumbnail(size, Image.Resampling.LANCZOS)
        #chart.save("static/starchart" + uid  + ".png")

        for key in results[3].keys():
            x = str(results[3][key])
            if not x.replace(".", "").isnumeric():
                results[3][key] = 0
        im = Image.open(path)
        im.thumbnail(size, Image.Resampling.LANCZOS)
        new_image_path = path
        if ".jpg" in path.lower() or ".jpeg" in path.lower():
            new_image_path = path.replace(".jpg", ".png").replace(".jpeg", ".png").replace(".JPG", ".png").replace(
                ".JPEG", ".png")
            picname = picname.replace(".jpg", ".png").replace(".jpeg", ".png").replace(".JPG", ".png").replace(
                ".JPEG", ".png")
            im.save(new_image_path)

        if results[0] == "Success":
            result = "Good job!"
            message = str(round(results[1],2)) + "%"
        else:
            result = "Oh no :("
            message = str(round(results[1],2)) + "%"

        return render_template("randomemotion.html",emotion=emotion, result = results[2], message = message, picname = "/static/" + picname, success = results[0], stats = results[3])
    else:
        emotions = ['Anger', 'Sadness', 'Disgust', 'Happiness', 'Fear', 'Surprise']
        emotion = random.choice(emotions)
        return render_template("randomemotion.html", emotion=emotion, result = None, message = None, picname = None, success = None, stats = {'happy': 0, 'angry': 0, 'sad' : 0, 'fear' : 0, 'surprise' : 0, 'disgust' :0 , 'neutral':0})

@app.route("/useremotion", methods=["POST", "GET"])
def useremotion():
    if request.method == "POST":
        uid = datetime.today().strftime("%x").replace('/', '-') + datetime.today().strftime("%X").replace(':', '-')
        emotion = request.form.get("emotion")
        path = None
        picname = None
        pic = flask.request.files['pic']
        if pic.filename == "":
            tmpurl = ""
            try:
                tmpurl = flask.request.values['backendimage'].split(';')[1].split(',')[1]
            except:
                return render_template("useremotion.html", emotion=emotion, result=None, message=None, picname=None,
                                       success=None,
                                       stats={'happy': 0, 'angry': 0, 'sad': 0, 'fear': 0, 'surprise': 0, 'disgust': 0,
                                              'neutral': 0})
            nparr = np.frombuffer(base64.b64decode(tmpurl), np.uint8)
            pic = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imwrite(os.getcwd() + "/static/" + "livepic" + uid + ".png", pic)
            path = os.getcwd() + "/static/" + "livepic" + uid + ".png"
            picname = "livepic" + uid + ".png"
        else:
            pic.save(os.getcwd() + "/static/" + pic.filename)
            path = os.getcwd() + "/static/" + pic.filename
            picname = pic.filename
        try:
            results = emotionAnalysis(path, emotion, False)
        except:
            results = emotionAnalysis(path, emotion, True)
        #results[3].write_image("static/starchart" + uid  + ".png")
        size = 700, 700
        #chart = Image.open("static/starchart" + uid  + ".png")  # Convert image into 500x500
        #chart.thumbnail(size, Image.Resampling.LANCZOS)
        #chart.save("static/starchart" + uid + ".png")

        im = Image.open(path)
        im.thumbnail(size, Image.Resampling.LANCZOS)
        new_image_path = path
        if ".jpg" in path.lower() or ".jpeg" in path.lower():
            new_image_path = path.replace(".jpg", ".png").replace(".jpeg", ".png").replace(".JPG", ".png").replace(
                ".JPEG", ".png")
            picname = picname.replace(".jpg", ".png").replace(".jpeg", ".png").replace(".JPG", ".png").replace(
                ".JPEG", ".png")
            im.save(new_image_path)

        if results[0] == "Success":
            result = "Good job!"
            message = str(round(results[1],2)) + "%"
        else:
            result = "Oh no :("
            message = str(round(results[1],2)) + "%"
        emotions = ['Anger', 'Sadness', 'Disgust', 'Happiness', 'Fear', 'Surprise']
        return render_template("useremotion.html", emotions = emotions, emotion = emotion, result = results[2], message = message, picname = "/static/" + picname, success = results[0], stats = results[3])
    else:
        emotions = ['Anger', 'Sadness', 'Disgust', 'Happiness', 'Fear', 'Surprise']
        return render_template("useremotion.html", emotions = emotions, emotion = None, result = None, message = None, picname = None, success = None, stats = {'happy': 0, 'angry': 0, 'sad' : 0, 'fear' : 0, 'surprise' : 0, 'disgust' :0 , 'neutral':0})

if __name__ == "__main__":
    #app.debug = True
    app.run()
