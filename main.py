
from fastapi import FastAPI, HTTPException, APIRouter
import analyzer

app = FastAPI(title="JobSentry: Scam Job Detector")
app.include_router(analyzer.router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set specific domain instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
