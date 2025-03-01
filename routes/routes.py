from controller.AccountController import AccountRouter;
from controller.ChatController import ChatRouter
from controller.UploadController import UploadRouter;

def routes(app):
    app.include_router(AccountRouter, prefix="/account")
    app.include_router(UploadRouter)
    app.include_router(ChatRouter)
