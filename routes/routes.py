from controller.AccountController import accountRouter;
from controller.ChatController import ChatRouter
from controller.UploadController import uploadRouter
from diInjector.diExtension import Container;

container = Container()

container.wire(modules=["controller.AccountController"])
container.wire(modules=["controller.UploadController"])
container.wire(modules=["controller.ChatController"])
def routes(app):
    app.include_router(accountRouter, prefix="/account")
    app.include_router(uploadRouter)
    app.include_router(ChatRouter)
