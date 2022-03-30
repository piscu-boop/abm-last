import sys
sys.path.append("..")

from asyncio import exceptions
from operator import lt
from webbrowser import get
from xmlrpc.client import Boolean
from pydantic import BaseModel, Field
from typing import Optional
import models
from routers import auth
from routers.auth import get_current_user, get_password_hash
from fastapi import APIRouter, Depends, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}} 
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title : str
    description : Optional[str]
    priority : int = Field(ge=1, lt=6, description="Priority must be between 1 to 5")
    complete : Boolean


""" esta funcion se utilizo para crear la base de datos, vacia."""

# @app.get("/")
# async def create_database():
#    return{"Database" : "Created :)"} 

@router.get("/Obtener_todos")
async def read_all(db: Session = Depends(get_db)): # --> Esta sentencia hace que la db sea de tipo 
# Session y que dependa de  la funcion de conseguir la base de datos.
    return db.query(models.Todos).all()

@router.get("/get_todo/{todo_id}")
async def get_todo_by_id(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise exceptions()
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first() # El id debe coincidir con el id ingresado. Con 
    # el metodo db.query estamos consultando a la base de datos! Usamos el first porque sabemos que el id es un primary key q es 
    # unico entonces cuando lo encuentra, ya dejara de recorrer el registro y lo devuelve :)
    if todo_model is not None:
        return todo_model
    raise raise_item_cannot_be_found_exception() # Usamos la funcion que creamos ya que aplica para lo mismo !

@router.post("/post_ToDo")
async def post_ToDo(todo: Todo, user: dict = Depends(get_current_user),
 db: Session = Depends(get_db)):
    if user is None:
        raise exceptions()
    todo_model = models.Todos() # Estamos creando una variable llamada todo que tendra los mismos atributos que Todos
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    # formamos el todo model y lo rellenamos con lo que escriba el usuario
    # lo agregamos a la database
    db.add(todo_model)
    # con el commit cerramos la transaccion, confirmandola y guardando todo en la db
    db.commit()
    succesfull_response()
    
@router.put("/update_todo/{todo_id}")
async def update_todo(todo_id : int, todo: Todo, user: dict = Depends(get_current_user),  db: Session = Depends(get_db)):
    # todo : Todo genera que todo,que es un registro nuevo, herede todo los atributos de la clase Todo
    if user is None:
        raise exceptions()
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).\
        filter(models.Todos.owner_id == user.get("id")).first()
    if todo_model is None:
        raise raise_item_cannot_be_found_exception()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()
    succesfull_response()

@router.delete("/{todo_id}")
async def delete_Todo(todo_id : int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise exceptions()
    todo_delete = db.query(models.Todos).filter(models.Todos.id == todo_id).\
        filter(models.Todos.owner_id == user.get("id")).first()
    if todo_delete is None:
        raise raise_item_cannot_be_found_exception()
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()

    
def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail="Item not found")

def succesfull_response():
        return{
        "status" : 200,
        "Transcription" : "Succesfull"
    }

    