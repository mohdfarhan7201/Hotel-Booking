from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, hotels, bookings
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LuxeStay API",
    description="Luxury Hotel Booking Platform API",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost:5173", # Vite default
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(hotels.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "Welcome to the LuxeStay API. Access /docs for Swagger UI."}
