from dependency_injector import containers, providers
from db.connection import dbConnection
from services.AccountService import AccountService
from services.UploadService import UploadService

class Container(containers.DeclarativeContainer):
    db = providers.Singleton(dbConnection)  
    account_service = providers.Factory(AccountService, db=db)
    upload_service = providers.Factory(UploadService, db=db)