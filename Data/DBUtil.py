import pyodbc
from flask import jsonify

from Data.Models import Attempts

def insertAttempt(connection_string, attempt):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Attempts (result, percentage, emotion_detected, target_emotion ,img,date) VALUES (?,?,?,?,?,?)"
        ,(attempt.result, attempt.percentage.replace('%',''), attempt.emotion_detected, attempt.target_emotion ,attempt.img, attempt.date)
    )

    conn.commit()
    cursor.close()
    conn.close()

def executeSelectQuery(connection_string, query):
    if("INSERT" in query.upper() or "UPDATE" in query.upper() or "DELETE" in query.upper() ):
        return jsonify({
         "status": "error",
         "message": "Invalid query, only SELECT queries are allowed"
        }), 400

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = []
        cols = []
        for column in cursor.description:
            cols.append(column[0])

        for row in cursor.fetchall():
            results.append(dict(zip(cols, row)))

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "answer": results,
        }), 200
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({
         "status": "error",
         "message": str(e)
        }), 400