from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..auth import get_current_active_user
from ..dependencies import get_db

router = APIRouter(
    prefix="/shops",
    tags=["shops"]
)

@router.post("/", response_model=schemas.Shop)
def create_shop_for_vendor(
    shop: schemas.ShopCreate,
    db: Session = Depends(get_db),
    current_user: models.Vendor = Depends(get_current_active_user)
):
    return crud.create_vendor_shop(db=db, shop=shop, vendor_id=current_user.id)


@router.get("/", response_model=List[schemas.Shop])
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shops = crud.get_shops(db, skip=skip, limit=limit)
    return shops


@router.get("/{shop_id}", response_model=schemas.Shop)
def read_shop(shop_id: int, db: Session = Depends(get_db)):
    db_shop = crud.get_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.put("/{shop_id}", response_model=schemas.Shop)
def update_shop(shop_id: int, shop: schemas.ShopCreate, db: Session = Depends(get_db), current_user: models.Vendor = Depends(get_current_active_user)):
    db_shop = crud.get_shop(db, shop_id=shop_id)
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    if db_shop.vendor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this shop") # Or 401 Unauthorized
    updated_shop = crud.update_shop(db, shop_id=shop_id, shop=shop)
    if not updated_shop:
         raise HTTPException(status_code=500, detail="Shop update failed")  #Or other appropriate error code
    return updated_shop

@router.delete("/{shop_id}", status_code=204) # Returns 204 No Content on success
def delete_shop(shop_id: int, db: Session = Depends(get_db), current_user: models.Vendor = Depends(get_current_active_user)):
    db_shop = crud.get_shop(db, shop_id=shop_id)
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    if db_shop.vendor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this shop")
    if not crud.delete_shop(db, shop_id=shop_id):
        raise HTTPException(status_code=500, detail="Shop deletion failed")
    return # 204 No Content implicitly returned

@router.get("/nearby/", response_model=List[schemas.Shop])
def search_nearby_shops(latitude: float, longitude: float, radius: float = 1.0, db: Session = Depends(get_db)):
    """
    Search for shops within a specified radius (in kilometers) of a given latitude and longitude.
    """
    earth_radius_km = 6371  # Radius of the Earth in kilometers

    distance = (
        earth_radius_km * func.acos(
            func.cos(func.radians(latitude))
            * func.cos(func.radians(models.Shop.latitude))
            * func.cos(func.radians(models.Shop.longitude) - func.radians(longitude))
            + func.sin(func.radians(latitude))
            * func.sin(func.radians(models.Shop.latitude))
        )
    )

    nearby_shops = db.query(models.Shop).filter(distance <= radius).all()

    return nearby_shops