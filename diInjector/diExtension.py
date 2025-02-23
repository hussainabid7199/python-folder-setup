from dependency_injector import containers, providers
from db.connection import dbConnection
from services.AccountService import AccountService

class Container(containers.DeclarativeContainer):
    db = providers.Singleton(dbConnection)  
    account_service = providers.Factory(AccountService, db=db)
