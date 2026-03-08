from fastapi import FastAPI
from app.api.verify import router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Proof-of-Skill Verification Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8003",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "https://supahire-ss.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
@app.get("/")
def root():
    return {
        "service": "SkillTrust Proof-of-Skill Engine",
        "status": "running"
    }
