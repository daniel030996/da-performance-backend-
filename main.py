from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI(title="DA PERFORMANCE Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Vehicle(BaseModel):
    make: Optional[str] = "Unknown"
    model: Optional[str] = ""
    year: Optional[int] = None
    engine: Optional[str] = None
    registration: Optional[str] = None

class DiagnosisRequest(BaseModel):
    vehicle: Vehicle
    problem: str

class Cause(BaseModel):
    title: str
    description: str
    likelihood: int
    fix: str
    cost_guidance: str

class DiagnosisResponse(BaseModel):
    summary: str
    severity: str
    estimated_cost_min: int
    estimated_cost_max: int
    likely_causes: List[Cause]
    sources: List[dict]

# Expanded realistic fault library (same as frontend but ready for real search later)
FAULTS = [
    {
        "keywords": ["grind", "grinding", "click", "clicking", "cv", "driveshaft", "full lock", "turning"],
        "summary": "Grinding or clicking on full lock is almost always a worn outer CV joint.",
        "severity": "medium",
        "cost": (180, 380),
        "causes": [
            {"title": "Worn outer CV joint", "description": "Classic noise under load on full lock. Boot often split.", "likelihood": 84, "fix": "Replace driveshaft or outer joint. Check the other side.", "cost_guidance": "£180–£380"},
            {"title": "Wheel bearing", "description": "Can sound similar; usually changes more with speed.", "likelihood": 16, "fix": "Check for play and replace hub if needed.", "cost_guidance": "£120–£250"}
        ]
    },
    {
        "keywords": ["start", "won't start", "no start", "crank", "battery", "slow crank"],
        "summary": "Starting problems are most often battery, connections or starter.",
        "severity": "medium",
        "cost": (40, 340),
        "causes": [
            {"title": "Battery or poor connections", "description": "Slow crank or single click. Very common.", "likelihood": 50, "fix": "Load-test battery and clean terminals.", "cost_guidance": "£60–£190"},
            {"title": "Starter motor", "description": "Loud click or grinding but no turnover.", "likelihood": 28, "fix": "Test and replace starter.", "cost_guidance": "£150–£340"}
        ]
    },
    # Add more as needed – the frontend already has a large set as fallback
]

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(req: DiagnosisRequest):
    text = req.problem.lower()
    vehicle_name = f"{req.vehicle.make} {req.vehicle.model}".strip()

    # Simple keyword match (can be replaced with real web search + LLM later)
    best = None
    best_score = 0
    for fault in FAULTS:
        score = sum(2 for kw in fault["keywords"] if kw in text)
        if score > best_score:
            best_score = score
            best = fault

    if not best:
        best = FAULTS[0]

    return DiagnosisResponse(
        summary=f"On the {vehicle_name}, {best['summary']}",
        severity=best["severity"],
        estimated_cost_min=best["cost"][0],
        estimated_cost_max=best["cost"][1],
        likely_causes=[Cause(**c) for c in best["causes"]],
        sources=[
            {"title": f"{req.vehicle.make} owner forums", "snippet": "Common real-world reports.", "type": "forum"},
            {"title": "Technical guides", "snippet": "Standard diagnostic steps.", "type": "forum"}
        ]
    )

@app.get("/")
def root():
    return {"status": "DA PERFORMANCE backend running", "endpoint": "/diagnose"}
