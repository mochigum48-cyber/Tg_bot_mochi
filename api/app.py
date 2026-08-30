from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import auth, books, saved, shop, ads

app = FastAPI(
    title="MM Digital Library API",
    version="1.0.0",
    description="Backend API for MM Digital Library Mini App"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later: restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(saved.router, prefix="/saved", tags=["Saved"])
app.include_router(shop.router, prefix="/shop", tags=["Shop"])
app.include_router(ads.router, prefix="/ads", tags=["Ads"])


@app.get("/")
async def root():
    return {
        "ok": True,
        "message": "MM Digital Library API is running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
