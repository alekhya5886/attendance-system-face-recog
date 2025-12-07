from flask import Flask, Response, render_template, request, redirect, url_for, jsonify
import cv2
import face_recognition
import numpy as np
import os
import pickle
from flask import flash
import pandas as pd
from datetime import datetime
import mysql.connector

app = Flask(__name__)

# -------------------------
# Config
# -------------------------
KNOWN_FACES_FILE = 'encodings.pkl'  # Pickle file with face encodings
ATTENDANCE_DIR = 'attendance_records'
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# -------------------------
# Load known faces
# -------------------------
if os.path.exists(KNOWN_FACES_FILE):
    with open(KNOWN_FACES_FILE, 'rb') as f:
        data = pickle.load(f)
        known_face_encodings = data['encodings']
        known_face_names = data['names']
    print(f"[Info] Loaded {len(known_face_names)} known faces")
else:
    known_face_encodings = []
    known_face_names = []
    print("[Warning] No encodings found. Add students first.")

# -------------------------
# Video capture
# -------------------------
cap = cv2.VideoCapture(0)  # Use default backend
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# -------------------------
# Database fetch
# -------------------------
def fetch_students():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="attendance_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT registration_number, name FROM students")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students
    except Exception as e:
        print(f"[DB Error] {e}")
        return []

# -------------------------
# Attendance storage
# -------------------------
def save_daily_attendance(attendance_list):
    today = datetime.now().date()
    filename = os.path.join(ATTENDANCE_DIR, f"attendance_{today}.xlsx")
    df = pd.DataFrame(attendance_list, columns=['Registration Number', 'Name', 'Date'])
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.drop_duplicates(subset=['Registration Number'], inplace=True)
    df.to_excel(filename, index=False)
    print(f"[Info] Attendance saved to {filename}")

# -------------------------
# Face recognition
# -------------------------
def detect_and_recognize(frame):
    recognized_students = []

    # Resize for faster recognition
    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        name = "Unknown"
        accuracy = 0

        if known_face_encodings:
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_idx = np.argmin(face_distances)
            accuracy = (1 - face_distances[best_idx]) * 100
            if face_distances[best_idx] < 0.6:
                name = known_face_names[best_idx]
                recognized_students.append({'name': name, 'accuracy': accuracy})

        # Scale coordinates to original frame
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, f"{name} ({accuracy:.1f}%)", (left, bottom+20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return frame, recognized_students

# -------------------------
# Generate frames for Flask
# -------------------------
def gen_frames():
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue

        annotated_frame, _ = detect_and_recognize(frame)

        ret2, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret2:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# -------------------------
# Flask routes
# -------------------------
@app.route('/')
def index():
    students = fetch_students()
    return render_template('index.html', students=students)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recognized_students')
def recognized_students():
    ret, frame = cap.read()
    recognized = []
    if ret and frame is not None:
        _, recognized = detect_and_recognize(frame)
    return jsonify({'recognized_students': [r['name'] for r in recognized]})

@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    selected = request.form.getlist('students')
    today = datetime.now().date()
    attendance_list = []

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="attendance_db"
        )
        cursor = conn.cursor()
        for reg_no in selected:
            cursor.execute("SELECT name FROM students WHERE registration_number=%s", (reg_no,))
            result = cursor.fetchone()
            if result:
                name = result[0]
                attendance_list.append((reg_no, name, today))
                cursor.execute("INSERT INTO attendance (registration_number, name, date) VALUES (%s, %s, %s)",
                               (reg_no, name, today))
        conn.commit()
        cursor.close()
        conn.close()

        save_daily_attendance(attendance_list)
        flash("✅ Attendance saved successfully!", "success")
        return redirect(url_for('index'))

    except Exception as e:
        print(f"[Error] {e}")
        return "Error saving attendance"



if __name__ == '__main__':
    app.run(debug=True)
