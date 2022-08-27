from .. import models
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..schemas import UserOut,UserCreate
from ..utils import hash
from ..database import engine,get_db

router =APIRouter(
    prefix="/users",
    tags = ["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    user.password = hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")

    return user