from fastapi import Depends, FastAPI, HTTPException, status


from .db import Base, engine
from app.tables import *
from app.router import *
from app.security import *
from app.auth import *
from app import modelos
from app.apisauth import *

app = FastAPI()

''' DB table Builder'''

Base.metadata.create_all(bind=engine) 

''' Creador de los routers (ordenado)'''


app.include_router(routerAccounts)
app.include_router(routerBayer)
app.include_router(routerBc_bp)
app.include_router(routerBc_icp)
app.include_router(routerbc_pers)
app.include_router(routerbj_icp)
app.include_router(routerbuyersjourney)
app.include_router(routerBuyingcomitee)
app.include_router(routerCamp_cont)
app.include_router(routerCamp_KPI)
app.include_router(routerCamp_pers)
app.include_router(routerCamp_stgs)
app.include_router(routerCampaign_goals)
app.include_router(routerCampaign)
app.include_router(routerCg_camp)
app.include_router(routercompanies)
app.include_router(routerCont_type)
app.include_router(routerContent)
app.include_router(routerdistr_channels)
app.include_router(routerIcp_ind)
app.include_router(routerIcp_tier)
app.include_router(routerIcp)
app.include_router(routerIndustries)
app.include_router(routerJobtitle)
app.include_router(routerKPI)
app.include_router(routerPersonas)
app.include_router(routerRole_bp)
app.include_router(routerServprod)
app.include_router(routerServprodcomp)
app.include_router(routerStages)
app.include_router(routertiers)



''' Security 
__JWTDUMMY__ = 'jwtDummy_'
@app.post("/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = abm_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": f'{__JWTDUMMY__}{user.username}', "token_type": "bearer"} '''
