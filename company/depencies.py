from fastapi import Header, HTTPException


async def get_token_header(internal_token: str = Header(...)):
    if internal_token != "allowed":
        # Allowed sera nuestra clave secreta para acceder a la informacion de companyes
        raise HTTPException(status_code=400, detail="Internal token header in")