from controller.AccountController import AccountRouter;
from controller.ChatController import ChatRouter
from controller.FindUserController import FindUserRouter
from controller.UploadController import UploadRouter
from controller.VerificationController import VerificationRouter;
from controller.UpdateUserController import UpdateUserRouter;
from controller.DeleteUserController import DeleteUserRouter;

def routes(app):
    app.include_router(AccountRouter, prefix="/account")
    app.include_router(UploadRouter)
    app.include_router(ChatRouter)
    app.include_router(VerificationRouter)
    app.include_router(FindUserRouter)
    app.include_router(UpdateUserRouter)
    app.include_router(DeleteUserRouter)