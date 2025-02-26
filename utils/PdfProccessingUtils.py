import re
from typing import List
import PyPDF2
import io
import pytesseract
from pdf2image import convert_from_bytes
from concurrent.futures import ThreadPoolExecutor
from utils.CheckPdfUtils import check_pdf_type


def extract_text_from_pdf(content: bytes) -> list:
    try:
        if not content or len(content) == 0:
            raise ValueError("Uploaded file is empty")

        pdf_file = io.BytesIO(content)
        check_pdf_type(pdf_file)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        if len(pdf_reader.pages) == 0:
            raise ValueError("PDF contains no pages")

        text_chunks = [page.extract_text() or "" for page in pdf_reader.pages]
        if any(text_chunks):
            return text_chunks

        # If no text, use OCR
        images = convert_from_bytes(content)
        with ThreadPoolExecutor() as executor:
            text_chunks = list(executor.map(pytesseract.image_to_string, images))

        return text_chunks

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []