from typing import Optional
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException



'''
    Loging with:
        user: admin 
        passwd: passwd
'''

__USERNAME__ = "abmmarket"

__JWTDUMMY__ = f'jwtDummy_{__USERNAME__}'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
# OAuth2PasswordRequestForm tiene atributos de uso común como 'nombre de usuario', 'contraseña' y 'alcance'.
# Después de verificar en la base de datos que el usuario existe, se crea un token de acceso para el usuario. 
# El token de acceso consta de datos que describen al usuario, sus límites de tiempo de acceso y los permisos 
# de alcance que se le asignan y que se codifica en un objeto compacto de tipo cadena, que es el token.

# Token_auth1 depende de OAuth2passwordBearer a traves del oauth2_scheme
def token_auth1(token: str=Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(401, "Invalid token")
        # Si el token no existe ya sea porque no ha sido creado o es ncorrecto el usuario, 
        # se levanta la excepcion de acceso restringido
    if  token != __JWTDUMMY__: # Si el token creado no se corresponde con el solicitado se levanta la exception
        raise HTTPException(401, "Invalid token")

def fake_hash_password(password: str):
    return "#swdedfer2sas_" + password

abm_users_db = {
    "admin": {
        "username": __USERNAME__,
        "full_name": "ABM MArketing User",
        "email": "",
        "hashed_password": "#swdedfer2sas_passwd",
        "disabled": False,
    },
}

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str