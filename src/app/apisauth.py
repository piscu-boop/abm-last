from app.router import *
from fastapi import Depends, FastAPI, HTTPException, status
from app.auth import *
from app import modelos

app = FastAPI()

@app.post("/auth/create_new_user")
async def create_new_user(create_user: Create_User, db: Session = Depends(get_db)):
    create_user_models = modelos.User()
    create_user_models.email = create_user.email
    create_user_models.username = create_user.username
    create_user_models.first_name = create_user.firstname
    create_user_models.last_name = create_user.lastname
    hash_password = get_password_hash(create_user.password)
    create_user_models.hashed_password = hash_password
    create_user_models.is_active = True

    db.add(create_user_models)
    db.commit()

@app.post("/token")
async def login_for_acces_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_expires = timedelta(minutes=20)
    # Todos los token deben tener si o si una fecha de expiracion 
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"token": token}
