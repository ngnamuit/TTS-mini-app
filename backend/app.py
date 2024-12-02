from fastapi import FastAPI

app = FastAPI(
    title="Management APIs",
    description="Main to manage apis",
    version="1.0.0",
)
@app.get("/")
async def root():
    return {"message": "Welcome to Main the place to manage APIs"}
