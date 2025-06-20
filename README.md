# 🧠 Replica – Multilingual PDF Translator with Layout Preservation

**Replica** is a web-based application that allows users to upload a PDF file in any language and receive an **English-translated replica**, preserving the original layout, formatting, tables, and text. It uses the **OpenAI GPT-4o** API for high-fidelity language translation and leverages **PyMuPDF** for layout-aware PDF processing.

---

## 🚀 Features

- 🌐 Translate PDFs in **any language** to **English**
- 🧱 Preserves **original layout**, including **tables**, **headers**, and **spacing**
- ⚡ Built on **FastAPI** for rapid, scalable performance
- 🤖 Powered by **OpenAI GPT-4o** for accurate translation
- 📥 Supports file upload and download via simple web UI
- 📊 Background task support using **Celery + Redis**
- 🖼️ OCR support for scanned PDFs (optional)

---

## 🏗️ Tech Stack

| Layer       | Technology      |
|-------------|-----------------|
| Backend     | FastAPI, Uvicorn |
| PDF Engine  | PyMuPDF (fitz), pdfplumber |
| Translation | OpenAI GPT-4o   |
| Queue       | Celery, Redis   |
| OCR (opt.)  | pytesseract, OpenCV |
| Deployment  | Docker, Docker Compose |

---
