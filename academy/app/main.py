from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "This Code Is Deployed To Server Using Jenkins Pipeline"}

