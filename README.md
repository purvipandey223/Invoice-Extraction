# InvoiceExtractor-Python

📄 A Python-based utility to extract structured data from Amazon and Flipkart invoice PDFs using text parsing — no third-party APIs, no OCR.

## 🚀 Features

- Extracts Order ID, Invoice Date, Seller, GSTIN from invoice headers
- Parses product lines (description, quantity, price, total) using full-text pattern matching
- Outputs clean, structured Excel files per invoice
- Fully offline and compliant with assignment rules (no cloud services used)

## 🧰 Tech Stack

- Python 3.x
- PyMuPDF (fitz)
- pandas
- re (regex)

## 📁 Folder Structure
├── Input_Folder/ # Place all invoice PDFs here
├── Output_Folder/ # Clean Excel files will be saved here
├── Coding_Folder/
│ └── extract_invoices_text_based.py
└── README.md


## ⚙️ How to Run

1. Install dependencies:
   ```bash
   pip install pymupdf pandas openpyxl
2. Place your invoice PDFs in Input_Folder
3.Run the script:
   python Coding_Folder/extract_invoices_text_based.py
4. Check Output_Folder for cleaned Excel files.

📌 Note

This tool is tuned for Amazon and Flipkart invoice formats.
If parsing fails, tweak the regular expressions in extract_products().

Made with ❤️ by Purvi Pandey
