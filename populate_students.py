import pandas as pd
import mysql.connector
import os
import face_recognition
import pickle

# ----------------------------
# Config
# ----------------------------
EXCEL_FILE = 'students.xlsx'
KNOWN_FACES_DIR = 'known_faces'
ENCODINGS_FILE = 'encodings.pkl'

# ----------------------------
# Load existing encodings
# ----------------------------
if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, 'rb') as f:
        data = pickle.load(f)
        known_face_encodings = data['encodings']
        known_face_names = data['names']
else:
    known_face_encodings = []
    known_face_names = []

# ----------------------------
# Read Excel with student info
# ----------------------------
df = pd.read_excel(EXCEL_FILE)
print(f"[Info] Read {len(df)} students from Excel")

# ----------------------------
# Connect to MySQL
# ----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="attendance_db"
)
cursor = conn.cursor()

# ----------------------------
# Insert students and encode faces
# ----------------------------
for index, row in df.iterrows():
    reg_no = str(row['RegNo'])
    name = row['Name']

    # Insert student if not exists
    cursor.execute("SELECT * FROM students WHERE registration_number=%s", (reg_no,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO students (registration_number, name) VALUES (%s, %s)",
            (reg_no, name)
        )
        print(f"[DB] Added student: {reg_no} - {name}")

    # Check if face already encoded
    if name not in known_face_names:
        img_path_jpg = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
        img_path_png = os.path.join(KNOWN_FACES_DIR, f"{name}.png")

        if os.path.exists(img_path_jpg):
            img_path = img_path_jpg
        elif os.path.exists(img_path_png):
            img_path = img_path_png
        else:
            print(f"[Warning] No image found for {name} in {KNOWN_FACES_DIR}")
            continue

        # Encode face
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
            print(f"[Info] Encoded face for {name}")
        else:
            print(f"[Warning] Could not encode face for {name}")

# Commit DB changes
conn.commit()
cursor.close()
conn.close()

# Save updated encodings
with open(ENCODINGS_FILE, 'wb') as f:
    pickle.dump({'encodings': known_face_encodings, 'names': known_face_names}, f)

print(f"[Info] Updated encodings saved to {ENCODINGS_FILE}")
print("[Info] Student population and face encoding complete!")
