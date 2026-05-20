from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.industry_routes import router as industry_router
from database import load_all_data

app = FastAPI(
    title="Trade Industry Insights API",
    description="Global trade data API — OEC dataset 2018–2024",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Loading trade data into memory...")
    load_all_data()
    print("Server ready ✓")

app.include_router(industry_router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "running",
        "docs": "/docs",
        "endpoints": [
            "/api/trade/companies",
            "/api/trade/manufacturers",
            "/api/trade/market-size",
            "/api/trade/exports",
            "/api/trade/imports",
            "/api/trade/end-industries",
            "/api/trade/countries",
            "/api/trade/industries",
            "/api/trade/years",
            "/api/trade/products",
        ]
    }