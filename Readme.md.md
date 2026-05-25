**🎓 Smart Notes AI System**

Smart Notes AI is an advanced educational platform designed to transform handwritten academic notes into structured digital learning assets. By leveraging cutting-edge OCR and Generative AI, the system automates the process of summarizing, cleaning, and testing knowledge from physical study materials.



**🚀 Key Features**

Handwritten OCR Pipeline: Utilizes PyMuPDF and EasyOCR to accurately extract text from handwritten images and multi-page PDF documents.



AI-Powered Content Analysis: Integrated with Google Gemini 1.5 Flash to perform spelling correction, grammatical cleaning, and logical summarization.



3-Column Interactive Dashboard:



Column 1 (Obtained Text): Displays the raw, original text extracted directly from the uploaded source.



Column 2 (Cleaned \& Summary): Features the AI-refined version of the notes alongside a concise conceptual summary.



Column 3 (Practice Quiz): Offers an interactive MCQ environment where users can test their knowledge and reveal answers upon submission.



Personalized Note Vault: Features a secure Flask-Login authentication system and an SQLite backend, ensuring that each user’s study materials are private and personalized.



Export to PDF: Allows users to generate and download professionally formatted PDF revision guides containing the summary and quiz for offline study.



🛠️ **Tech Stack**

Frontend: HTML5, CSS3 (Modern Glassmorphism UI), JavaScript.



Backend: Python, Flask.



AI/ML: Google Gemini API, EasyOCR.



Database: SQLite3.



Libraries: PyMuPDF (fitz) for PDF processing, ReportLab for dynamic PDF generation.



📦 **Installation \& Setup**

Clone the Repository:



Bash

git clone https://github.com/your-username/smart-notes-ai.git

cd smart-notes-ai



2\.  \*\*Install Required Dependencies\*\*:

&#x20;   ```bash

&#x20;   pip install flask flask-login google-genai easyocr pymupdf reportlab

Initialize the Database:



Bash

python database.py



4\.  \*\*Configure API Access\*\*:

&#x20;   \*   Obtain a Gemini API Key from Google AI Studio.

&#x20;   \*   Update the `api\_key` variable in `ai\_engine.py`.



5\.  \*\*Run the Application\*\*:

&#x20;   ```bash

&#x20;   python app.py

🛡️ **Security \& Privacy**

The project follows professional development standards by utilizing a .gitignore file to prevent sensitive database files (.db) and private API keys from being exposed in public repositories.

