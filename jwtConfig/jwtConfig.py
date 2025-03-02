import os
from dotenv import load_dotenv
import jwt
import datetime

dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class JWTConfig:
    @staticmethod
    def generate_token(email: str, user_id: str, expires_in: int = 360000) -> str:
        payload = {
            "sub": user_id,
            "email": email,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in),
            "iss": "smart-pdf-solution"
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
