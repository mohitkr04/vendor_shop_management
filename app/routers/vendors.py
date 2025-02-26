from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..auth import create_access_token, get_current_active_user
from ..dependencies import get_db

router = APIRouter(
    prefix="/vendors",
    tags=["vendors"]
)


@router.post("/", response_model=schemas.Vendor)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    db_vendor = crud.get_vendor_by_email(db, email=vendor.email)
    if db_vendor:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_vendor(db=db, vendor=vendor)


@router.get("/me", response_model=schemas.Vendor)
async def read_users_me(current_user: models.Vendor = Depends(get_current_active_user)):
    return current_user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    vendor = crud.get_vendor_by_email(db, email=form_data.username)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not crud.verify_password(form_data.password, vendor.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": vendor.email})
    return {"access_token": access_token, "token_type": "bearer"}