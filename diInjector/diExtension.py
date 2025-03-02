from dependency_injector import containers, providers
from db.connection import dbConnection
from services.AccountService import AccountService
from services.DeleteUserService import DeleteUserService
from services.UpdateUserService import UpdateUserService
from services.UploadService import UploadService
from services.ChatService import ChatService
from services.VerificationService import VerificationService
from services.FindUserService import FindUserService

class Container(containers.DeclarativeContainer):
    db = providers.Singleton(dbConnection)  
    account_service = providers.Factory(AccountService, db=db)
    upload_service = providers.Factory(UploadService, db=db)
    chat_service = providers.Factory(ChatService, db=db)
    verification_service = providers.Factory(VerificationService, db=db)
    finduser_service = providers.Factory(FindUserService, db=db)
    updateuser_service = providers.Factory(UpdateUserService, db=db)
    deleteuser_service = providers.Factory(DeleteUserService, db=db)
