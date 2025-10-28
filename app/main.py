from fastapi import FastAPI

app = FastAPI(title="CORPORATION / OFFICE")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"app": "CORPORATION / OFFICE", "status": "ready"}
