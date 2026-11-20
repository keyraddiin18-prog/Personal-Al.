import io
from pathlib import Path
from pypdf import PdfReader


# ==========================================
# KEYRADDIIN PERSONAL AI V2.0
# PDF PROCESSING SYSTEM
# ==========================================

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

MAX_PAGES = 100


# ==========================================
# VALIDATE PDF FILE
# ==========================================

def validate_pdf(file_data):

    if not file_data:

        raise ValueError("PDF file is empty.")

    if len(file_data) > MAX_FILE_SIZE:

        raise ValueError(
            "PDF file is too large. Maximum size is 20 MB."
        )

    if not file_data.startswith(b"%PDF-"):

        raise ValueError(
            "Invalid PDF file. Please upload a valid PDF."
        )

    return True


# ==========================================
# EXTRACT TEXT FROM PDF BYTES
# ==========================================

def extract_pdf_from_bytes(file_data):

    validate_pdf(file_data)

    try:

        pdf_stream = io.BytesIO(file_data)

        reader = PdfReader(pdf_stream)

        # CHECK ENCRYPTION
        if reader.is_encrypted:

            raise ValueError(
                "This PDF is password protected."
            )

        # CHECK PAGE COUNT
        total_pages = len(reader.pages)

        if total_pages == 0:

            raise ValueError(
                "This PDF has no pages."
            )

        if total_pages > MAX_PAGES:

            raise ValueError(
                "PDF exceeds the maximum limit of 100 pages."
            )

        extracted_pages = []

        # EXTRACT TEXT PAGE BY PAGE
        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            text = page.extract_text() or ""

            extracted_pages.append({

                "page": page_number,

                "text": text.strip()

            })

        full_text = "\n\n".join(

            f"PAGE {item['page']}\n{item['text']}"

            for item in extracted_pages

            if item["text"]

        )

        if not full_text.strip():

            raise ValueError(
                "No readable text found. "
                "This may be a scanned PDF."
            )

        return {

            "success": True,

            "filename": "uploaded.pdf",

            "total_pages": total_pages,

            "extracted_pages": extracted_pages,

            "text": full_text,

            "characters": len(full_text),

            "message": "PDF processed successfully."

        }

    except ValueError:

        raise

    except Exception as error:

        print("PDF PROCESSING ERROR:", error)

        raise ValueError(
            "Unable to process this PDF file."
        )


# ==========================================
# EXTRACT TEXT FROM PDF FILE PATH
# ==========================================

def extract_pdf_text(file_path):

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(
            "PDF file not found."
        )

    if not path.is_file():

        raise ValueError(
            "Invalid PDF file path."
        )

    if path.stat().st_size > MAX_FILE_SIZE:

        raise ValueError(
            "PDF file is too large. Maximum size is 20 MB."
        )

    with open(path, "rb") as file:

        file_data = file.read()

    result = extract_pdf_from_bytes(file_data)

    result["filename"] = path.name

    return result


# ==========================================
# GET PDF INFORMATION
# ==========================================

def get_pdf_info(file_data):

    result = extract_pdf_from_bytes(file_data)

    return {

        "filename": result["filename"],

        "total_pages": result["total_pages"],

        "characters": result["characters"],

        "status": "processed"

    }


# ==========================================
# PREPARE PDF CONTENT FOR AI
# ==========================================

def prepare_pdf_for_ai(pdf_text):

    if not pdf_text or not pdf_text.strip():

        raise ValueError(
            "No PDF text available."
        )

    return f"""
You are KEYRADDIIN PERSONAL AI.

The user has uploaded a PDF document.

Use the following PDF content to answer
the user's questions accurately.

Explain difficult concepts clearly.

Support Afaan Oromo and English.

PDF DOCUMENT CONTENT:

{pdf_text}
"""


# ==========================================
# PDF SYSTEM INFORMATION
# ==========================================

def pdf_system_info():

    return {

        "system": "KEYRADDIIN PDF READER",

        "version": "2.0",

        "status": "active",

        "maximum_file_size": "20 MB",

        "maximum_pages": MAX_PAGES,

        "supported_format": "PDF"

    }


print("KEYRADDIIN PDF READER LOADED!")