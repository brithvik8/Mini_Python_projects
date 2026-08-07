# Professional PDF Merger & Splitter Desktop Application

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, highly responsive desktop utility application built in Python using **CustomTkinter** and **pypdf** to merge multiple PDF documents, extract custom page selections (ranges), split files into individual pages, and rotate PDF layouts.

---

## 🌟 Key Highlights
- **Fluid & Responsive UI**: Runs all PDF writing operations asynchronously on background threads to ensure the interface never freezes, even when processing large files.
- **Modern Aesthetics**: Native dark-mode styled frames built with modern typography, smooth transition tabs, and rounded corners.
- **Custom Page Selection Parsing**: Resilient inputs parsing (e.g. `1-3, 5, 8-10`) with bounds guards, error messages, and format validations.
- **100% Test Coverage**: The core engine is decoupled from the user interface and covers edge cases with an automated unit test suite.

---

## 📁 Folder Structure
```text
PDF Merger - Splitter/
│
├── services/
│   ├── __init__.py
│   └── pdf_service.py          # Core logic (using pypdf)
│
├── ui/
│   ├── __init__.py
│   └── app.py                  # CustomTkinter GUI layout
│
├── tests/
│   ├── __init__.py
│   └── test_pdf_service.py     # pytest unit tests
│
├── main.py                     # Entry point (boots the GUI)
├── requirements.txt            # Package dependencies
├── .gitignore                  # Git exclude configurations
└── README.md                   # Documentation guide
```

---

## 🚀 Installation & Setup

### Prerequisites
Make sure Python 3.12 (or the latest stable version) is installed.

### 1. Clone or Move to Workspace
Open your terminal in the root folder of this project:
```bash
cd "PDF Merger - Splitter"
```

### 2. Install Dependencies
Install all package requirements:
```bash
python -m pip install -r requirements.txt
```

---

## 💻 How to Run the Application
Run the bootstrapper script:
```bash
python main.py
```

### User Guide
1. **Merge PDFs Tab**:
   - Click **+ Add PDFs** to import your files.
   - Select a file in the list and use **Move Up** / **Move Down** to customize the merging order, or **Remove** to delete it.
   - Click **Browse** under *Output Path* to select where you want to save the new merged file.
   - Click **Merge PDFs**.
2. **Split PDF Tab**:
   - Select an input file.
   - In **Extract Ranges**, enter the custom page range (e.g. `1-4, 6`) and choose the file output path. Click **Extract Selected Pages**.
   - In **Split All Pages**, select a folder directory. Click **Split All Pages** to split each page into its own individual PDF document.
3. **Rotate Pages Tab**:
   - Choose a file, select the rotation angle (90, 180, or 270 degrees), choose the output path, and click **Rotate PDF Pages**.

---

## 🧪 Testing the Project
Run automated pytest tests:
```bash
python -m pytest
```

---

## 📦 Packaging to Standalone Executable (.exe)
You can compile this Python desktop app into a standalone, single-file Windows executable (`.exe`) so users do not need Python installed to run it.

1. Install `pyinstaller`:
   ```bash
   python -m pip install pyinstaller
   ```
2. Build the application using PyInstaller:
   ```bash
   pyinstaller --noconsole --onefile --name="PDFMergerSplitter" main.py
   ```
3. Locate the final executable in the generated `dist/` directory.

---

## 🛠️ Technology Stack
- **GUI Framework**: `CustomTkinter`
- **PDF Manipulation**: `pypdf`
- **Asynchronous Execution**: `threading`
- **Testing**: `pytest`
- **Build Tool**: `PyInstaller`

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
