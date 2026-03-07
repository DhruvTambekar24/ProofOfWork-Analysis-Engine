from fastapi import FastAPI
from app.api.verify import router

app = FastAPI(title="Proof-of-Skill Verification Engine")

app.include_router(router)