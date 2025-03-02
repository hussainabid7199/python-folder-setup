from cerberus import Validator

Registerschema = {
    "name": {"type": "string", "minlength": 6, "maxlength": 30, "required": True},
    "email": {"type": "string", "regex": r"^[\w\.-]+@[\w\.-]+\.\w+$", "required": True},
    "password": {"type": "string", "minlength": 6, "maxlength": 14, "required": True},
}

registervalidator = Validator(Registerschema)
