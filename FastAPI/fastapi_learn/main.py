from fastapi import FastAPI

app = FastAPI(title="Dummy Proj")

@app.get("/")
def health_check():
    return {"message": "Service is Running"}

@app.get("/student_name/{name}")
def get_student_name(name: str):
    return {"message": f"Welcome to FastAPI {name}"}

@app.get("/age_student")
def get_student_age(month: int, year: int):
    return {"month": month,
            "year": year,
            "message": f"You was born in {month}/{year}"}
