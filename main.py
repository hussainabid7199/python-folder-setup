from diInjector.diExtension import Container 
from fastapi import FastAPI
from fastapi import APIRouter, Depends

# Initialize Dependency Injection container
container = Container()
router = APIRouter()
# Create FastAPI app
app = FastAPI()

# Wire dependencies
container.wire(modules=["controller.AccountController"])

# Register router
app.include_router(router, prefix="/account")

print("Router registered successfully!")
