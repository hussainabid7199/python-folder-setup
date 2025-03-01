from dependency_injector import containers, providers
from bucket.AWSBucket import awsBucket
from bucket.PineConeBucket import pineCone
from db.connection import dbConnection
from services.AccountService import AccountService
from services.UploadService import UploadService

class Container(containers.DeclarativeContainer):
    db = providers.Singleton(dbConnection) 
    aws_bucket = providers.Singleton(awsBucket)
    pine_cone = providers.Singleton(pineCone)
     
    account_service = providers.Factory(AccountService, db=db)
    upload_service = providers.Factory(UploadService, db=db, aws_bucket=aws_bucket, pine_cone=pine_cone)

