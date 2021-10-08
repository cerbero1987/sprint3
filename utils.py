import re
from validate_email import validate_email

pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
user_reguex = "^[a-zA-Z0-9_.-]+$"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'


def isEmailValid(email):
    #error = 'Correo invalido'
    is_valid = validate_email(email)

    return is_valid


def isUsernameValid(user):
    #error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
    if re.search(user_reguex, user):
        return True
    else:
        return False


def isPasswordValid(password):
    #error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
    if re.search(pass_reguex, password):
        return True
    else:
        return False
