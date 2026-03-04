from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Demo Application New!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}