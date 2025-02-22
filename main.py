from fastapi import FastAPI
from middleware.ClientIdMiddleware import ClientIdMiddleware
from routes.routes import routes
from diInjector.diExtension import Container
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(ClientIdMiddleware)

container = Container()

routes(app)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Server running at http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
