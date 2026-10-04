from fastapi import  APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = User(
        name =user_data.name,
        email=user_data.email
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
