import os
import sys
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse
from dtos.UploadDto import UploadDto
from interface.IUploadInterface import IUploadService
from models.UploadModel import UploadModel
from utils.CheckFileTypeUtils import check_pdf_type
from utils.ChunkTextUtils import chunk_text
from utils.EmbeddingChunksUtils import generate_and_store_chunks_embedding
from utils.PdfProccessingUtils import extract_text_from_pdf
from utils.OpenSearchUtils import index_document
from bucket.AWSBucket import AWSbucket
import logging

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)

bucket_name = os.getenv("BUCKET_NAME")

# Configure Logger (only logs to terminal)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class UploadService(IUploadService):
    def __init__(self, db=None):
        aws_bucket = AWSbucket()

        self.s3_client = aws_bucket.get_aws_bucket()

        # Get S3 client with proper error handling
        if not self.s3_client:
            logger.error("Failed to initialize AWS S3 client")
            raise HTTPException(status_code=500, detail="Failed to initialize AWS S3 client")

        self.bucket_name = bucket_name

    async def upload(self, file: UploadFile, model: UploadModel) -> UploadDto:
        try:
            logger.info(f"Received file: {file.filename} for processing.")
            check_pdf_type(file)
            await file.seek(0)
            content = await file.read()

            # Extract text from the PDF
            extracted_text_chunks = extract_text_from_pdf(content)

            if not extracted_text_chunks or not isinstance(extracted_text_chunks, list):
                logger.warning(f"No text found in uploaded PDF: {file.filename}")
                raise HTTPException(
                status_code=400, detail="No text found in the uploaded PDF"
            )

            file_path = f"uploads/{file.filename}"  # S3 path
            try:
                self.s3_client.put_object(Bucket=self.bucket_name, Key=file_path, Body=content)
                logger.info(f"Successfully uploaded file '{file.filename}' to S3 at {file_path}")
            except Exception as e:
                logger.error(f"Failed to upload file '{file.filename}' to S3: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Failed to upload file to S3: {str(e)}")
            chunk_size = 500
            text_chunks = chunk_text(extracted_text_chunks, chunk_size=chunk_size)

            if not text_chunks:
                logger.error(f"Failed to extract text chunks for file: {file.filename}")
                raise HTTPException(status_code=400, detail="Failed to extract text chunks")

            # Generate and store embeddings
            # embedding_response = generate_and_store_chunks_embedding(file_id, text_chunks)
            logger.info(f"Generating embeddings for {len(text_chunks)} chunks.")
            embedding_response = generate_and_store_chunks_embedding(file_path, text_chunks)

            if embedding_response["status"] == "error":
                logger.error(f"Embedding error: {embedding_response['error']}")
                raise HTTPException(status_code=500, detail=embedding_response["error"])
            
            # Index chunks into OpenSearch
            indexed_chunks = []
            i=0
            for chunk in text_chunks:
                document = {
                    "file_id": f"file_id_{file_path}_chunk_{i}",
                    "filename": file.filename,
                    "chunk": chunk
                }
                i+=1

                index_response = index_document(document)
                
                if index_response["status"] == "error":
                    logger.error(f"OpenSearch indexing failed for chunk: {chunk[:50]}...")
                    raise HTTPException(status_code=500, detail="Error indexing chunk in OpenSearch")

                indexed_chunks.append(chunk)
            logger.info(f"Successfully processed and uploaded PDF '{file.filename}' with {len(text_chunks)} chunks.")
            return JSONResponse(
            content={
                "status": "success",
                "num_chunks": len(text_chunks),
                "file_id": file_path,
                "message": f"Processed and uploaded PDF '{file.filename}' successfully",
                "chunks": text_chunks[:5],
            },
            status_code=200,
            )

        except HTTPException as e:
            logger.error(f"HTTP Exception: {e.detail}", exc_info=True)
            raise e
