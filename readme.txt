# ![Face Recognition Attendance](https://img.shields.io/badge/Face-Recognition-blue) Face Recognition Attendance System

> Real-Time Attendance Management using Face Recognition
> *Python · Flask · OpenCV · face_recognition · MySQL*

[![Python Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Demo](#demo)
* [Tech Stack](#tech-stack)
* [Installation](#installation)
* [Usage](#usage)
* [Database Setup](#database-setup)
* [Folder Structure](#folder-structure)
* [Contributing](#contributing)
* [Team](#team)
* [License](#license)

---

## Overview

This project implements a **real-time attendance system** that uses a webcam to detect and recognize faces of students. Attendance is **automatically recorded** in a MySQL database and saved as daily Excel sheets.

* Detects faces using `face_recognition` and `OpenCV`.
* Compares against stored encodings (`encodings.pkl`) for recognition.
* Web-based interface using **Flask**.
* Attendance records saved in both **database** and **Excel files**.

---

## Features

* Real-time face detection and recognition.
* Automatic attendance logging.
* Daily Excel reports for attendance.
* Web interface to view and save attendance.
* Configurable for multiple users and classes.

---

## Demo

![Demo Screenshot](https://user-images.githubusercontent.com/yourusername/demo-screenshot.png)
*Web interface showing recognized students and live webcam feed.*

---

## Tech Stack

| Component            | Details                    |
| -------------------- | -------------------------- |
| **Language**         | Python 3.11                |
| **Web Framework**    | Flask                      |
| **Face Recognition** | face_recognition, OpenCV   |
| **Data Handling**    | pandas, pickle             |
| **Database**         | MySQL                      |
| **Frontend**         | HTML/CSS (Flask templates) |

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/attendance-system-face-recog.git
cd attendance-system-face-recog
```

2. **Create and activate virtual environment**

```bash
python -m venv venv_face
# Windows PowerShell
.\venv_face\Scripts\Activate.ps1
# Windows CMD
.\venv_face\Scripts\activate
# Linux / macOS
source venv_face/bin/activate
```

3. **Upgrade pip**

```bash
pip install --upgrade pip
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Install face_recognition_models**

```bash
pip install git+https://github.com/ageitgey/face_recognition_models
```

> ⚠️ Use **NumPy < 2.0** to avoid compatibility issues:
> `pip install numpy==1.26.0`

---

## Usage

1. Run the Flask app:

```bash
python app.py
```

2. Open browser:

```
http://127.0.0.1:5000/
```

3. View live webcam feed and recognized students.
4. Click **Save Attendance** to log daily attendance.

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

## Folder Structure

```
face-recog-main/
├── app.py                   # Flask app
├── encode_faces.py          # Generate face encodings
├── encodings.pkl            # Known face encodings
├── attendance_records/      # Daily attendance Excel files
├── templates/               # HTML templates
│   └── index.html
├── static/                  # CSS/JS assets
├── requirements.txt         # Dependencies
├── venv_face/               # Virtual environment (ignore in Git)
└── README.md
```

> 💡 Add `venv_face/` and large models to `.gitignore` to avoid pushing large files to GitHub.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Open a Pull Request.

---

## Team

* [**Alekhya Madiraju**](https://github.com/alekhya5886)
  CSE - AIML, GITAM University
  [amadiraj2@gitam.in](mailto:amadiraj2@gitam.in)

* [*Add other members here if any*]

---

## License

This project is licensed under the [MIT License](LICENSE).
Feel free to use, modify, and distribute with attribution.
