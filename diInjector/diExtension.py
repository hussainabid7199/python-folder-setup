from dependency_injector import containers, providers
from db.connection import dbConnection
from services import AccountService  # Adjust import based on your setup

class Container(containers.DeclarativeContainer):
    db = providers.Singleton(dbConnection)  # Assuming you have a DB connection class
    account_service = providers.Factory(AccountService, db=db)
