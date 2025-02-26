from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_vendor(db: Session, vendor_id: int):
    return db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()


def get_vendor_by_email(db: Session, email: str):
    return db.query(models.Vendor).filter(models.Vendor.email == email).first()


def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vendor).offset(skip).limit(limit).all()


def create_vendor(db: Session, vendor: schemas.VendorCreate):
    hashed_password = get_password_hash(vendor.password)
    db_vendor = models.Vendor(name=vendor.name, email=vendor.email, hashed_password=hashed_password)
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor


def create_vendor_shop(db: Session, shop: schemas.ShopCreate, vendor_id: int):
    db_shop = models.Shop(**shop.dict(), vendor_id=vendor_id)
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop


def get_shops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Shop).offset(skip).limit(limit).all()


def get_shop(db: Session, shop_id: int):
    return db.query(models.Shop).filter(models.Shop.id == shop_id).first()

def update_shop(db: Session, shop_id: int, shop: schemas.ShopCreate):
    db_shop = db.query(models.Shop).filter(models.Shop.id == shop_id).first()
    if db_shop:
        for key, value in shop.dict().items():
            setattr(db_shop, key, value)
        db.commit()
        db.refresh(db_shop)
    return db_shop

def delete_shop(db: Session, shop_id: int):
    db_shop = db.query(models.Shop).filter(models.Shop.id == shop_id).first()
    if db_shop:
        db.delete(db_shop)
        db.commit()
        return True
    return False