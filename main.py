from fastapi import FastAPI, HTTPException
from exceptions.HttpException import http_exception_handler
from middleware.ClientIdMiddleware import ClientIdMiddleware
from routes.routes import routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

#app.add_middleware(ClientIdMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)

routes(app)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Server running at http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
