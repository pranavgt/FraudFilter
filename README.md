# FraudFilter

A simple scam-detection tool to help protect people (especially seniors) from online fraud, phishing, and scam messages.

📖 Overview

Our project is a scam detection tool for seniors. Users can either paste text or upload a screenshot of a message. The app extracts text with OCR, checks it against scam keywords like “urgent” or “wire transfer,” and shows a verdict. It also stores a history of all checks so family members can review past messages and spot scam patterns.

Fraud Filter is a lightweight tool that checks suspicious emails, texts, or call transcripts for common scam patterns such as:

Urgent language (“ACT NOW!”, “final notice”)

Demands for unusual payment methods (gift cards, crypto, wire transfers)

Fake authority claims (IRS, FBI, Amazon “support”)

Threatening language (lawsuit, warrant, arrest)

Suspicious links that don’t match the brand

Phone number requests

It produces a risk score and a simple explanation of why the message looks dangerous.

🚀 Features

Rule-based scam detection (transparent & easy to tune)

Risk levels: 🟢 Low, 🟠 Caution, 🔴 High

Clear “Why we flagged it” breakdown for each message

Two ways to run:

Command line app (paste text → get a score)

Streamlit web app (simple browser interface)

## 🛠 Tech Stack

- **Backend Framework**: [Flask](https://flask.palletsprojects.com/)  
  Lightweight Python web framework for routing and server logic.

- **OCR**: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) via [pytesseract](https://pypi.org/project/pytesseract/)  
  Extracts text from uploaded images/screenshots.

- **Image Processing**: [Pillow (PIL)](https://python-pillow.org/)  
  Handles image formats and preprocessing before OCR.

- **Database**: [SQLite](https://www.sqlite.org/)  
  File-based database for storing message checks and verdicts.

- **Templating**: [Jinja2](https://jinja.palletsprojects.com/)  
  Used by Flask to render dynamic HTML templates (`index.html`, `history.html`).

- **Styling**: Custom **CSS**  
  Lightweight red-accent UI for forms, verdicts, and history tables.

- **Version Control**: [Git](https://git-scm.com/) + [GitHub](https://github.com/)  
  For source control and collaboration.

- **AI Integration**: [OpenAI API](https://platform.openai.com/)  
  For enhanced scam-risk classification (🟢 Low, 🟠 Caution, 🔴 High).


