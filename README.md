
# KTM Information Extraction

## Project Description
KTM Information Extraction is an OCR extraction project designed to extract information from student ID cards (Kartu Tanda Mahasiswa - KTM) at Universitas Teknologi Yogyakarta. This project utilizes Tesseract for optical character recognition (OCR) and FastAPI for creating the API.

## Installation Instructions

### Prerequisites
- Python 3.x
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- FastAPI

### Steps
1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/ktm-information-extraction.git
    cd ktm-information-extraction
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install Tesseract OCR**:
    Follow the instructions on the [Tesseract GitHub page](https://github.com/tesseract-ocr/tesseract) to install Tesseract OCR on your system.

## Usage

To run the project, use the following command:
```bash
uvicorn app.main:app --reload
```

This will start the FastAPI server. You can then access the API documentation at `http://127.0.0.1:8000/docs`.

## Features
- Extracts student information from KTM cards using OCR.
- Provides an API endpoint to submit images and receive extracted information.
- Supports various image formats.

## Technologies Used
- Python
- FastAPI
- Tesseract OCR

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Submit a pull request.
