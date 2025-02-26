from fastapi import FastAPI
from .database import create_tables
from .routers import vendors, shops
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) - configure as needed for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - VERY permissive, restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
async def startup_event():
    create_tables()


app.include_router(vendors.router)
app.include_router(shops.router)


@app.get("/")
async def root():
    return {"message": "Vendor and Shop Management API"}