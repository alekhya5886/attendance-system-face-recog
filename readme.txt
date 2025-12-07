
# Face Recognition Attendance System

A Python-based **attendance management system** that uses **face recognition** to detect and record student attendance. Built with **Flask**, **OpenCV**, **face_recognition**, and **MySQL**.

---

## **Features**

* Real-time face recognition using webcam
* Automatic attendance recording in **MySQL database**
* Daily attendance saved as **Excel files**
* Web interface to view students and mark attendance
* Basic popup notification when attendance is saved

---

## **Prerequisites**

* Python 3.11.x
* Git
* MySQL Server
* Visual Studio Build Tools (for compiling dlib if needed)

---

## **Project Setup**

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

* **Windows (PowerShell)**:

```powershell
.\venv_face\Scripts\Activate.ps1
```

* **Windows (CMD)**:

```cmd
.\venv_face\Scripts\activate
```

* **Linux/macOS**:

```bash
source venv_face/bin/activate
```

4. **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ **Important:** Do **not** commit `venv_face` to GitHub. Use `.gitignore` to exclude it.

---

## **Database Setup**

1. Start MySQL server.
2. Create a database:

```sql
CREATE DATABASE attendance_db;
```

3. Create `students` and `attendance` tables:

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

## **Face Encodings**

1. Add student images to generate encodings.
2. Run your encoding script (e.g., `encode_faces.py`) to create `encodings.pkl`.
3. Ensure `encodings.pkl` is in the project root.

---

## **Running the App**

```bash
python app.py
```

* Open a browser at `http://127.0.0.1:5000/`
* You should see the student list and webcam feed
* Recognized faces will be highlighted
* Save attendance using the form, and a **popup** confirms success

---

## **Notes for Large Files**

* Do **not** commit your virtual environment (`venv_face`) or large binary files.
* `shape_predictor_68_face_landmarks.dat` (~95 MB) is required by `face_recognition_models`.
  Options:

  1. Use **Git LFS** to store large files.
  2. Download it dynamically in your code instead of pushing to GitHub.

Example `.gitignore` snippet:

```
venv_face/
__pycache__/
*.pyc
*.pyo
*.pyd
*.xlsx
*.dat
```

---

## **Dependencies**

* Flask==2.3.2
* OpenCV==4.8.1.78
* face_recognition==1.3.0
* face_recognition_models (install via Git)
* numpy>=1.25.0, <2.0 (to avoid incompatibility)
* pandas>=2.1.1
* mysql-connector-python>=9.5.0
* Pillow

---

## **Tips / Troubleshooting**

1. **dlib build errors** (on Windows):

   * Install Visual Studio Build Tools (C++ Desktop workload)
   * Or use precompiled wheel for Python 3.11

2. **NumPy 2.x errors:**

   * Use NumPy `<2` to avoid crashes with OpenCV/face_recognition:

   ```bash
   pip install numpy==1.26.0
   ```

3. **Face Recognition Models not found**:

```bash
pip install git+https://github.com/ageitgey/face_recognition_models
```

---

## **License**

MIT License
