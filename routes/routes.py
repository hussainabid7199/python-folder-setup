from controller.AccountController import AccountRouter;
from controller.UploadController import UploadRouter;

def routes(app):
    app.include_router(AccountRouter, prefix="/account")
    app.include_router(UploadRouter)
