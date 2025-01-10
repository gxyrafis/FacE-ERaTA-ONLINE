import os
import random
import flask
from flask import Flask, redirect, url_for, render_template, request
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
        pic = flask.request.files['pic']
        pic.save(os.getcwd() + "/static/" + pic.filename)
        path = os.getcwd() + "/static/" + pic.filename
        picname = pic.filename
        try:
            results = emotionAnalysis(path, "T", False)
        except:
            results = emotionAnalysis(path, "T", True)
        results[3].write_image("static/starchart.png")
        size = 700, 700
        chart = Image.open("static/starchart.png")  # Convert image into 500x500
        chart.thumbnail(size, Image.Resampling.LANCZOS)
        chart.save("static/starchart.png")

        im = Image.open(path)
        im.thumbnail(size, Image.Resampling.LANCZOS)
        new_image_path = path
        if ".jpg" in path.lower() or ".jpeg" in path.lower():
            new_image_path = path.replace(".jpg", ".png").replace(".jpeg", ".png").replace(".JPG", ".png").replace(
                ".JPEG", ".png")
            picname = picname.replace(".jpg", ".png").replace(".jpeg", ".png").replace(".JPG", ".png").replace(
                ".JPEG", ".png")
            im.save(new_image_path)
        message = "Our AI thought you were displaying " + results[
                        2] + " with an accuracy of " + str(round(results[1], 2)) + "%"
        return render_template("result.html",result = None, message = message, picname = picname)
    else:
        return render_template("training.html")

@app.route("/random", methods=["POST", "GET"])
def randomemotion():
    if request.method == "POST":
        emotion = request.form.get("emotioninput")
        pic = flask.request.files['pic']
        pic.save(os.getcwd() + "/static/" + pic.filename)
        path = os.getcwd() + "/static/" + pic.filename
        picname = pic.filename
        try:
            results = emotionAnalysis(path, emotion, False)
        except:
            results = emotionAnalysis(path, emotion, True)
        results[3].write_image("static/starchart.png")
        size = 700, 700
        chart = Image.open("static/starchart.png")  # Convert image into 500x500
        chart.thumbnail(size, Image.Resampling.LANCZOS)
        chart.save("static/starchart.png")

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
            message = "You have achieved an accuracy of " + str(round(results[1],2)) + "% at displaying " + emotion
        else:
            result = "Oh no :("
            message = "You have only achieved an accuracy of " + str(round(results[1],2)) + "% at displaying " + emotion + ". Our AI thought you were displaying " + results[2] + " instead."

        return render_template("result.html",result = result, message = message, picname = picname, success = results[0])
    else:
        emotions = ['Anger', 'Sadness', 'Disgust', 'Happiness', 'Fear', 'Surprise']
        emotion = random.choice(emotions)
        return render_template("randomemotion.html", emotion=emotion)

@app.route("/useremotion", methods=["POST", "GET"])
def useremotion():
    if request.method == "POST":
        emotion = request.form.get("emotion")
        pic = flask.request.files['pic']
        pic.save(os.getcwd() + "/static/" + pic.filename)
        path = os.getcwd() + "/static/" + pic.filename
        picname = pic.filename
        try:
            results = emotionAnalysis(path, emotion, False)
        except:
            results = emotionAnalysis(path, emotion, True)
        results[3].write_image("static/starchart.png")
        size = 700, 700
        chart = Image.open("static/starchart.png")  # Convert image into 500x500
        chart.thumbnail(size, Image.Resampling.LANCZOS)
        chart.save("static/starchart.png")

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
            message = "You have achieved an accuracy of " + str(round(results[1],2)) + "% at displaying " + emotion
        else:
            result = "Oh no :("
            message = "You have only achieved an accuracy of " + str(round(results[1],2)) + "% at displaying " + emotion + ". Our AI thought you were displaying " + results[2] + " instead."

        return render_template("result.html",result = result, message = message, picname = picname, success = results[0])
    else:
        emotions = ['Anger', 'Sadness', 'Disgust', 'Happiness', 'Fear', 'Surprise']
        return render_template("useremotion.html", emotions=emotions)

if __name__ == "__main__":
    app.run()