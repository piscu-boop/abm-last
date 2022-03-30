
from fastapi import FastAPI, Depends
from database import engine
import models
from routers import auth, todos
from company import companyapis, depencies


app = FastAPI(title="ToDo project :)")

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companyapis.router, 
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(depencies.get_token_header)],
    responses={418: {"description": "Internal use only"}}
)


