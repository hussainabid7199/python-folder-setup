import os
import sys
from dotenv import load_dotenv
from fastapi import File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from dtos.UploadDto import UploadDto
from interface.IUploadInterface import IUploadService
from models.UploadModel import UploadModel
from utils.CheckFileTypeUtils import check_pdf_type
from utils.ChunkTextUtils import chunk_text
from utils.PdfProccessingUtils import extract_text_from_pdf
from utils.EmbeddingChunksUtils import Embedding

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

bucket_name = os.getenv("BUCKET_NAME")


class UploadService(IUploadService):
    def __init__(self, db, aws_bucket, pine_cone):
        self.db = db
        self.aws_bucket = aws_bucket
        self.pine_cone = pine_cone
        self.s3_client = self.aws_bucket
        self.bucket_name = bucket_name

    async def upload(self, file: UploadFile = File(...)) -> dict:
        try:
            print("in upload service")
            check_pdf_type(file)

            content = await file.read()

            # Extract text from the PDF
            extracted_text_chunks = extract_text_from_pdf(content)

            if not extracted_text_chunks or not isinstance(extracted_text_chunks, list):
                raise HTTPException(
                    status_code=400, detail="No text found in the uploaded PDF"
                )

            file_id = self.s3_client.upload_file(file.filename, file.content)
            chunk_size = 500
            text_chunks = chunk_text(extracted_text_chunks, chunk_size=chunk_size)

            if not text_chunks:
                raise HTTPException(
                    status_code=400, detail="Failed to extract text chunks"
                )

            # Generate and store embeddings
            embedding_response = Embedding.generate_and_store_chunks_embedding(
                file_id, text_chunks
            )

            if embedding_response["status"] == "error":
                raise HTTPException(status_code=500, detail=embedding_response["error"])

            return JSONResponse(
                content={
                    "status": "success",
                    "num_chunks": len(text_chunks),
                    "file_id": file_id,
                    "message": f"Processed and uploaded PDF '{file.filename}' successfully",
                    "chunks": text_chunks[:5],
                },
                status_code=200,
            )

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(e)}"
            )
