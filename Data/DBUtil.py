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

def executeSelectQuery(connection_string, query):
    if("INSERT" in query.upper() or "UPDATE" in query.upper() or "DELETE" in query.upper() ):
        return False

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        conn.commit()

        return True
    except Exception as e:
        print(e)
        return False