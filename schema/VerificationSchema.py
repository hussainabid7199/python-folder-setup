from cerberus import Validator

VerificationSchema = {
    "email": {"type": "string", "regex": r"^[\w\.-]+@[\w\.-]+\.\w+$", "required": True},
    "code": {"type": "string", "maxlength": 6, "required": True},
}

verificationvalidator = Validator(VerificationSchema)