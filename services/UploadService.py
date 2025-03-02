import os
import sys
from dotenv import load_dotenv
from fastapi import File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from dtos.UploadDto import UploadDto
from interface.IUploadInterface import IUploadService
from utils.CheckFileTypeUtils import check_pdf_type
from utils.ChunkTextUtils import chunk_text
from utils.EmbeddingChunksUtils import embed
from utils.OpenSearchUtils import index_document
import logging

from utils.PdfProccessingUtils import extract_text_from_pdf

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

bucket_name = os.getenv("BUCKET_NAME")

# Configure Logger (only logs to terminal)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class UploadService(IUploadService):
    def __init__(self, db, aws_bucket, pine_cone, open_search):
        self.db = db
        self.pine_cone = pine_cone
        self.open_search = open_search
        self.s3_bucket = aws_bucket

    async def upload(self, file: UploadFile) -> UploadDto:
        try:
            logger.info(f"Received file: {file.filename} for processing.")
            check_pdf_type(file)
            await file.seek(0)
            content = await file.read()

            file_path = f"uploads/{file.filename}"  # S3 path

            try:
                self.s3_bucket.get_aws_bucket().put_object(
                    Bucket=bucket_name, Key=file_path, Body=content
                )
                logger.info(
                    f"Successfully uploaded file '{file.filename}' to S3 at {file_path}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to upload file '{file.filename}' to S3: {e}", exc_info=True
                )
                raise HTTPException(
                    status_code=500, detail=f"Failed to upload file to S3: {str(e)}"
                )

            chunk_size = 500
            extracted_text_chunks = extract_text_from_pdf(content)

            if not extracted_text_chunks or not isinstance(extracted_text_chunks, list):
                logger.warning(f"No text found in uploaded PDF: {file.filename}")
                raise HTTPException(
                    status_code=400, detail="No text found in the uploaded PDF"
                )

            text_chunks = chunk_text(extracted_text_chunks, chunk_size=chunk_size)

            if not text_chunks:
                logger.error(f"Failed to extract text chunks for file: {file.filename}")
                raise HTTPException(
                    status_code=400, detail="Failed to extract text chunks"
                )

            logger.info(f"Generating embeddings for {len(text_chunks)} chunks.")

            if file_path and text_chunks:
                embedding_response = embed.generate_and_store_chunks_embedding(
                    self, file_path, text_chunks
                )

            if embedding_response["status"] == "error":
                logger.error(f"Embedding error: {embedding_response['error']}")
                raise HTTPException(status_code=500, detail=embedding_response["error"])

            indexed_chunks = []
            for chunk in text_chunks:
                document = {
                    "file_id": file_path,
                    "filename": file.filename,
                    "chunk": chunk,
                }

                index_response = index_document(document)

                if index_response["status"] == "error":
                    logger.error(
                        f"OpenSearch indexing failed for chunk: {chunk[:50]}..."
                    )
                    raise HTTPException(
                        status_code=500, detail="Error indexing chunk in OpenSearch"
                    )

                indexed_chunks.append(chunk)

            logger.info(
                f"Successfully processed and uploaded PDF '{file.filename}' with {len(text_chunks)} chunks."
            )

            response = UploadDto(
                num_chunks=len(text_chunks),
                file_name= file.filename,
                file_id=file_path,
                chunks=text_chunks[:5],
            )

            return response;

        except HTTPException as e:
            logger.error(f"HTTP Exception: {e.detail}", exc_info=True)
            raise e
