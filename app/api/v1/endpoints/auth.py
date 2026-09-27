from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.user import Token, UserCreate, UserResponse
from app.database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import app.database.models as models
from sqlalchemy.orm import Session

router = APIRouter()

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.User).filter(models.User.email == user_in.email).first()
    )
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )

    new_user = models.User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        subscription_credits=5,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == form_data.username)
        .first()
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user