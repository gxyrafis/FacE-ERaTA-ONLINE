import pyodbc
from Data.Models import Attempts

def insertAttempt(connection_string, attempt):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Attempts (result, percentage, emotion_detected, target_emotion ,img,date) VALUES (?,?,?,?,?,?)"
        ,(attempt.result, attempt.percentage.replace('%',''), attempt.emotion_detected, attempt.target_emotion ,attempt.img, attempt.date)
    )

    conn.commit()