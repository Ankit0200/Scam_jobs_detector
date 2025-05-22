
from fastapi import FastAPI, HTTPException, APIRouter
import analyzer

app = FastAPI(title="JobSentry: Scam Job Detector")
app.include_router(analyzer.router)