from controller.AccountController import router

def routes(app):
    app.include_router(router, prefix="/account")
