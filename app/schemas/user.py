from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    subscription_credits: int
    purchased_credits: int
    subscription_tier: str

    class Config:
        from_attributes = True    

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"    

class GoogleLogin(BaseModel):
    id_token: str                    