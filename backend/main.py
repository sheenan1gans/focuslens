study_stats = {"Focus Time": 0, "Distraction" : 0}

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from passlib.hash import bcrypt
from database.database import engine, SessionLocal

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
    time_spent : int
    subject: str

@app.get("/")
def home():
    return {"message": "Server running"}
    
@app.post("/track")
def track_activity(data: TrackData):
    print(f"Recieved URL from Extension: {data.url}")
    db = SessionLocal()

study_sites = ["stackoverflow.com", "github.com", "coursera.org", "docs.python.org"]

is_study = any(site in data.url for site in study_sites)

def classify_url(url:str):
       url = data.url.lower()
       if is_study:
        category= "Focus Time"
        message= "Keep it up!" 
       else:
        category= "Distraction" 
        message= "Get back to work!"

        return{
        "status": "success", 
        "category": category, 
        "message": message,
        "current_total": study_stats
    }

study_stats[category] += 1
print(f"{category} : {url}")
print(f"Current Stats: {study_stats}")

new_log = StudyLog (url= data.url, category=category)
db.add(new_log)
db.commit()
db.refresh(new_log)
db.close()


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
