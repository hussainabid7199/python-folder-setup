from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from dtos.VerificationDto import VerificationDto
from models.VerificationModel import VerificationModel
from interface.IVerificationInterface import IVerificationService
from schema.VerificationSchema import verificationvalidator
from jwtConfig.jwtConfig import JWTConfig

class VerificationService(IVerificationService):
    def __init__(self, db):
        self.db = db
        self.db = self.db.get_collection("users")

    def verify(self, model: VerificationModel) -> VerificationDto:
        model_dict = model.model_dump()
        if not verificationvalidator.validate(model_dict):
            raise HTTPException(status_code=500, detail=verificationvalidator.errors)

        exsisting_user = self.db.find_one({"email": model.email})

        if not exsisting_user:
            raise HTTPException(status_code=404, detail="User not found with this email")

        verification_data = exsisting_user.get("verification_code", {})
        stored_code = verification_data.get("code")
        stored_expiry_time = verification_data.get("expiryTime") 

        aware_expiry_time = stored_expiry_time.replace(tzinfo=timezone.utc)

        if datetime.now(timezone.utc) > aware_expiry_time:
            raise HTTPException(status_code=404, detail="Otp expired please log in again")

        if stored_code != model.code:
            raise HTTPException(
                status_code=404, detail="Otp code not match"
            )

        self.db.update_one({"_id": exsisting_user["_id"]}, {
           "$set": {
               "is_verified": True,
                "verification_code": {
                    "code": "",
                    "expiryTime": datetime.now() + timedelta(seconds=0),
                }
           }
        })

        token = JWTConfig.generate_token(
            exsisting_user["email"], exsisting_user["id"]
        )
        verifyDto = VerificationDto(email=model.email, token=token)
        return verifyDto
