import jwt
import datetime

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

class JWTConfig:
    @staticmethod
    def generate_token(email: str, user_id: str, expires_in: int = 3600) -> str:
        payload = {
            "sub": user_id,
            "email": email,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in),
            "iss": "smart-pdf-solution"
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token