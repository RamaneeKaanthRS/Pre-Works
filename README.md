# Pre-Works
Pre-Wroks is a basic Command-line Software for Pre-Production works in Film-Making even Media

# 🎬 Film Preproduction CLI

A lightweight, human-friendly **command-line tool** for film preproduction.  
Write stories, screenplays, create characters, plan shots, save/load projects, and export everything into a formatted PDF — all from the terminal.

---

## ✨ Features

### 📖 Story Editor
Write the full story inside the terminal.  
End input with a single `.` on a new line.

### 🎬 Screenplay Editor
Enter screenplay text in plain form.  
The software automatically formats screenplay structure during PDF export.

### 👥 Character Manager
Create and manage:
- Name  
- Age  
- Characteristics  
- Movie  
- Most-used hand  

### 🎥 Shot Division
Define each shot with:
- Camera  
- Lens  
- Focal length  
- Aperture  
- Shutter  
- ISO  
- Movement  
- Duration  
- Description  

### 💾 Save & Load Projects
Projects are stored as `.fpproj` JSON files.

### 📄 PDF Export
Exports:
- Title page  
- Story  
- Screenplay  
- Characters  
- Shot list  

Requires:
pip install reportlab

---

## 📦 Installation

### 1. Install Python 3.8+
Ensure Python is installed.

### 2. Download the script
Save the program as:
pre-works.py

### 3. Install PDF support (Optional)
pip install reportlab

### 4. Run the program
python pre-works.py

---

## 🧭 Usage Guide

When launched, you will see:

Film Preproduction — Untitled
Edit metadata
Edit story
Edit screenplay
Characters
Shots
Save
Load
Export PDF
Quit
Choose:

### Menu Options

#### 1) Edit Metadata
Update Title and Author.

#### 2) Edit Story
Enter text → finish with a single `.` on a new line.

#### 3) Edit Screenplay
Same input method as story.

#### 4) Characters Menu
a) Add
b) List
c) Delete
d) Back
#### 6) Save Project
Save your work to `.fpproj`.

#### 7) Load Project
Load an existing `.fpproj`.

#### 8) Export PDF
Generates a formatted PDF with all project sections.

#### 9) Quit
Exit the program.

---

## 📁 Project Format
Projects are stored as JSON:
.fpproj

---

## ❤️ About
This tool is built to be minimal, clean, and human-friendly — perfect for filmmakers, writers, and students.

"""

path = Path("/mnt/data/README.md")
path.write_text(readme_text, encoding="utf-8")

"/mnt/data/README.md"
