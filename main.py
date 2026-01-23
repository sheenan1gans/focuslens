study_stats = {"Focus Time": 0, "Distraction" : 0}


from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from passlib.hash import bcrypt 

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrackData(BaseModel):
    url:str

@app.get("/")
def home():
    return {"message": "Server running"}

study_sites = ["stackoverflow.com", "github.com", "coursera.org", "docs.python.org"]
study_stats = {"Study": 0, "Distraction": 0}
    
@app.post("/track")
def track_activity(data: TrackData):
    print(f"Recieved URL from Extension: {data.url}")
    url = data.url.lower()

    is_study = any(site in url for site in study_sites)

    if is_study:
        category= "Study"
        message= "Keep it up!" 
    else:
        category= "Distraction" 
        message= "Get back to work!"
    
    study_stats[category] += 1
    print(f"{category} : {url}")
    print(f"Current Stats: {study_stats}")

    return {
        "status": "success", 
        "category": category, 
        "message": message,
        "current_total": study_stats
    }



class UserSignUp(BaseModel):
    username : str = Field(... , min_length=5, max_length= 15)
    email: EmailStr
    age : int = Field(gt = 0, lt=110)
    password : str = Field(..., min_length= 8)
    

class UserOut(BaseModel):
    username: str
    email: EmailStr
    age : int

fake_db = []

@app.post("/signup", response_model=UserOut)
def signup(user: UserSignUp):
    h = bcrypt.hash(user.password)

    new_user = {
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "hashed_password": h
    }

    fake_db.append(new_user)

    print(f"Database: {fake_db}")
    
    return UserOut (
    username=user.username,
    email=user.email,
    age=user.age
)
