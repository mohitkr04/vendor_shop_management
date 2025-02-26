from pydantic import BaseModel, ConfigDict

class VendorBase(BaseModel):
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class VendorCreate(VendorBase):
    password: str

class Vendor(VendorBase):
    id: int

class ShopBase(BaseModel):
    name: str
    owner: str
    business_type: str
    latitude: float
    longitude: float
    model_config = ConfigDict(from_attributes=True)

class ShopCreate(ShopBase):
    pass

class Shop(ShopBase):
    id: int
    vendor_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None