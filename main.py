from diInjector.diExtension import Container 
from fastapi import FastAPI
from controller.AccountController import router

app = FastAPI()

# Initialize Dependency Injection container
container = Container()
# Create FastAPI app

# Wire dependencies
container.wire(modules=["controller.AccountController"])

# Register router
app.include_router(router, prefix="/account")

print("Router registered successfully!")
