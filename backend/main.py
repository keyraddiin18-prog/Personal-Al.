# ==========================================
# KEYRADDIIN PERSONAL AI V2.0
# COMPLETE BACKEND SYSTEM
# ==========================================

import os

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from typing import Optional


from ai_engine import ai

from database import (
    init_db,
    create_chat,
    save_message,
    get_chat_history,
    get_all_chats,
    delete_chat,
    database_info
)

from pdf_processor import (
    extract_pdf_from_bytes,
    prepare_pdf_for_ai
)


# ==========================================
# APPLICATION
# ==========================================

app = FastAPI(

    title="KEYRADDIIN PERSONAL AI",

    description="Personal AI Assistant",

    version="2.0"

)


# ==========================================
# CORS CONFIGURATION
# ==========================================

origins = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5500,http://127.0.0.1:5500"
)

allowed_origins = [
    origin.strip()
    for origin in origins.split(",")
    if origin.strip()
]

app.add_middleware(

    CORSMiddleware,

    allow_origins=allowed_origins,

    allow_credentials=False,

    allow_methods=["GET", "POST", "DELETE"],

    allow_headers=["Content-Type"]

)


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

init_db()


# ==========================================
# REQUEST MODELS
# ==========================================

class ChatRequest(BaseModel):

    message: str

    chat_id: Optional[int] = None


class PDFQuestionRequest(BaseModel):

    pdf_text: str

    question: str


# ==========================================
# HOME
# ==========================================

@app.get("/")
async def home():

    return {

        "name": "KEYRADDIIN PERSONAL AI",

        "version": "2.0",

        "status": "running"

    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
async def health():

    return {

        "success": True,

        "status": "healthy",

        "ai": "KEYRADDIIN AI ENGINE",

        "version": "2.0"

    }


# ==========================================
# AI CHAT
# ==========================================

@app.post("/chat")
async def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:

        raise HTTPException(

            status_code=400,

            detail="Message cannot be empty."

        )

    if len(message) > 12000:

        raise HTTPException(

            status_code=400,

            detail="Message is too long."

        )

    try:

        chat_id = request.chat_id

        # CREATE NEW CHAT
        if chat_id is None:

            chat_id = create_chat(

                title=message[:40]

            )

        # SAVE USER MESSAGE
        save_message(

            chat_id,

            "user",

            message

        )

        # GENERATE AI RESPONSE
        response = await ai.generate_response(message)

        # SAVE AI RESPONSE
        save_message(

            chat_id,

            "assistant",

            response

        )

        return {

            "success": True,

            "chat_id": chat_id,

            "message": message,

            "response": response

        }

    except Exception as error:

        print("CHAT ERROR:", error)

        raise HTTPException(

            status_code=500,

            detail="AI processing failed."

        )


# ==========================================
# GET ALL CHATS
# ==========================================

@app.get("/chats")
async def chats():

    try:

        return {

            "success": True,

            "chats": get_all_chats()

        }

    except Exception as error:

        print("CHAT LIST ERROR:", error)

        raise HTTPException(

            status_code=500,

            detail="Could not load chats."

        )


# ==========================================
# GET CHAT HISTORY
# ==========================================

@app.get("/chats/{chat_id}")
async def chat_history(chat_id: int):

    try:

        return {

            "success": True,

            "chat_id": chat_id,

            "messages": get_chat_history(chat_id)

        }

    except Exception as error:

        print("CHAT HISTORY ERROR:", error)

        raise HTTPException(

            status_code=500,

            detail="Could not load chat history."

        )


# ==========================================
# DELETE CHAT
# ==========================================

@app.delete("/chats/{chat_id}")
async def remove_chat(chat_id: int):

    try:

        deleted = delete_chat(chat_id)

        return {

            "success": deleted,

            "message": (

                "Chat deleted."

                if deleted

                else "Chat not found."

            )

        }

    except Exception as error:

        print("DELETE CHAT ERROR:", error)

        raise HTTPException(

            status_code=500,

            detail="Could not delete chat."

        )


# ==========================================
# PDF UPLOAD
# ==========================================

@app.post("/pdf/upload")
async def upload_pdf(file: UploadFile = File(...)):

    filename = file.filename or ""

    if not filename.lower().endswith(".pdf"):

        raise HTTPException(

            status_code=400,

            detail="Only PDF files are supported."

        )

    try:

        file_data = await file.read(
            20 * 1024 * 1024 + 1
        )

        if len(file_data) > 20 * 1024 * 1024:

            raise HTTPException(

                status_code=413,

                detail="PDF file is too large. Maximum is 20 MB."

            )

        result = extract_pdf_from_bytes(file_data)

        if not result.get("success"):

            raise HTTPException(

                status_code=400,

                detail=result.get(
                    "message",
                    "Could not process PDF."
                )

            )

        return {

            "success": True,

            "filename": filename,

            "total_pages": result["total_pages"],

            "characters": result["characters"],

            "text": result["text"]

        }

    except HTTPException:

        raise

    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)

        )

    except Exception as error:

        print("PDF ERROR:", error)

        raise HTTPException(

            status_code=500,

            detail="PDF processing failed."

        )

    finally:

        await file.close()


# ==========================================
# ASK QUESTIONS ABOUT PDF
# ==========================================

@app.post("/pdf/ask")
async def ask_pdf(request: PDFQuestionRequest):

    pdf_text = request.pdf_text.strip()

    question = request.question.strip()

    if not pdf_text:

        raise HTTPException(

            status_code=400,

            detail="PDF text is empty."

        )

    if not question:

        raise HTTPException(

            status_code=400,

            detail="Question cannot be empty."

        )

    if len(pdf_text) > 80000:

        raise HTTPException(

            status_code=400,

            detail="PDF text is too long."

        )

    try:

        context = prepare_pdf_for_ai(pdf_text)

        prompt = f"""

You are KEYRADDIIN PERSONAL AI.

Answer the user's question using the supplied PDF.

PDF CONTENT:

{context}

USER QUESTION:

{question}

INSTRUCTIONS:

1. Use the PDF as your main source.
2. Explain difficult concepts clearly.
3. Support Afaan Oromo and English.
4. Give examples when helpful.
5. If the answer is not in the PDF,
   clearly say so.
6. Do not invent information.

"""

        response = await ai.generate_response(prompt)

        return {

            "success": True,

            "question": question,

            "response": response

        }

    except Exception as error:

        print("PDF AI ERROR:", error)

        raise HTTPException(

            status_code=500,

            detail="PDF AI processing failed."

        )


# ==========================================
# API INFORMATION
# ==========================================

@app.get("/api/info")
async def api_info():

    try:

        return {

            "application": "KEYRADDIIN PERSONAL AI",

            "version": "2.0",

            "database": database_info(),

            "features": [

                "Gemini AI Chat",

                "JSON AI Memory",

                "SQLite Chat History",

                "PDF Upload",

                "PDF Text Extraction",

                "PDF AI Questions",

                "Bilingual Support"

            ]

        }

    except Exception as error:

        print("API INFO ERROR:", error)

        raise HTTPException(

            status_code=500,

            detail="Could not retrieve API information."

        )


# ==========================================
# STARTUP MESSAGE
# ==========================================

print("====================================")

print("KEYRADDIIN PERSONAL AI BACKEND")

print("VERSION 2.0")

print("GEMINI AI SYSTEM READY")

print("JSON MEMORY SYSTEM READY")

print("SQLITE DATABASE READY")

print("PDF READER SYSTEM READY")

print("====================================")