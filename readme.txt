# Face Recognition Attendance System

> Real-Time Face Recognition · Attendance Management · Flask Web Interface
> *Built with Python, OpenCV, face_recognition, and MySQL*

---

## Table of Contents

* [Overview](#overview)
* [Problem Statement](#problem-statement)
* [Hardware & Software Setup](#hardware--software-setup)
* [Project Structure](#project-structure)
* [Installation & Setup](#installation--setup)
* [Running the Application](#running-the-application)
* [Database Setup](#database-setup)
* [Attendance Storage](#attendance-storage)
* [Observations](#observations)
* [Team Members](#team-members)
* [License](#license)

---

## Overview

This project implements a **real-time attendance system** using face recognition. Students’ faces are detected via webcam, recognized against known face encodings, and attendance is recorded automatically in a **MySQL database**. The system also saves **daily attendance Excel files** for record-keeping.

---

## Problem Statement

> Build a real-time system to recognize students from webcam video,
> mark attendance automatically, and store records both in a database and Excel files.

---

## Hardware & Software Setup

| Component      | Details                                                                     |
| -------------- | --------------------------------------------------------------------------- |
| CPU            | Intel® Core™ i5 or higher                                                   |
| GPU (optional) | Any GPU supported by OpenCV/face_recognition                                |
| OS             | Windows 10/11, Linux, or macOS                                              |
| Python         | 3.11.x                                                                      |
| Frameworks     | Flask · OpenCV · face_recognition · numpy · pandas · mysql-connector-python |
| Database       | MySQL                                                                       |
| Input          | Webcam (or recorded video)                                                  |

---

## Project Structure

```
face-recog-main/
├── app.py                   # Main Flask app
├── test.py                  # Test scripts for modules
├── encode_faces.py          # Script to generate face encodings
├── encodings.pkl            # Pickle file with known face encodings
├── attendance_records/      # Folder to store daily attendance Excel files
├── templates/               # HTML templates for Flask
│   └── index.html
├── static/                  # CSS/JS if any
├── requirements.txt         # Python dependencies
├── venv_face/               # Virtual environment (exclude from Git)
└── README.md
```

---

## Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/attendance-system-face-recog.git
cd attendance-system-face-recog
```

2. **Create a virtual environment**

```bash
python -m venv venv_face
```

3. **Activate the virtual environment**

* Windows (PowerShell):

```powershell
.\venv_face\Scripts\Activate.ps1
```

* Windows (CMD):

```cmd
.\venv_face\Scripts\activate
```

* Linux/macOS:

```bash
source venv_face/bin/activate
```

4. **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ Use **NumPy < 2.0** to avoid compatibility issues with OpenCV and face_recognition:

```bash
pip install numpy==1.26.0
```

5. **Install face_recognition_models**:

```bash
pip install git+https://github.com/ageitgey/face_recognition_models
```

---

## Running the Application

```bash
python app.py
```

* Open browser at `http://127.0.0.1:5000/`
* Webcam feed shows live video with recognized faces
* Attendance can be saved via the web interface with a popup confirmation

---

## Database Setup

1. Start MySQL server.
2. Create database:

```sql
CREATE DATABASE attendance_db;
```

3. Create tables:

```sql
CREATE TABLE students (
    registration_number VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registration_number VARCHAR(50),
    name VARCHAR(100),
    date DATE
);
```

---

## Attendance Storage

* Recognized students are logged into **MySQL database**.
* Daily attendance is saved in `attendance_records/attendance_YYYY-MM-DD.xlsx`.
* Duplicate entries are automatically removed per day.

---

## Observations

* Real-time recognition works reliably with small-to-medium class sizes.
* For large classes, GPU acceleration (if available) can improve speed.
* `encodings.pkl` must be updated whenever new students are added.
* Web interface allows quick attendance marking and immediate feedback.

---

## Team Members

* [*Alekhya Madiraju*](https://github.com/alekhya5886)
  CSE - AIML, GITAM University
  [amadiraj2@gitam.in](mailto:amadiraj2@gitam.in)

* [*Your teammate*]
  (Add additional team members here if any)

---

## License

This project is licensed under the [MIT License](LICENSE).
Feel free to use, modify, and distribute with attribution.

