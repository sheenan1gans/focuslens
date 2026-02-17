study_stats = {"Focus Time": 0, "Distraction" : 0}

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from passlib.hash import bcrypt
from database.database import engine, SessionLocal, Base
from database.models import StudyLog, User

app = FastAPI()
db = SessionLocal()
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
    
def classify_url(url:str):
       url = url.lower()

       study_sites = ["stackoverflow.com", "github.com", "coursera.org", "docs.python.org"]
       is_study = any(site in url for site in study_sites)

       if is_study:
        category= "Focus Time"
        message= "Keep it up!" 
       else:
        category= "Distraction" 
        message= "Get back to work!"

class TrackData(BaseModel):
    url: str
    user_id: int

@app.post("/track")
def track_activity(data: TrackData):
    print(f"Recieved URL from Extension: {data.url}")
    db = SessionLocal()

    category, message = classify_url(data.url)
    
    study_stats[category] += 1
    print(f"{category} : {url}")
    print(f"Current Stats: {study_stats}")

    new_log = StudyLog (user_id=data.user_id, url= data.url, category=category)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    db.close()

    return{
        "status": "success", 
        "category": category, 
        "message": message,
        "current_total": study_stats
    }
       

class UserSignUp(BaseModel):
    username : str = Field(... , min_length=5, max_length= 15)
    email: EmailStr
    age : int = Field(gt = 0, lt=110)
    password : str = Field(..., min_length= 3)
    
class UserOut(BaseModel):
    username: str
    email: EmailStr
    age : int


@app.post("/signup", response_model=UserOut)
def signup(user: UserSignUp):
    h = bcrypt.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        age=user.age,
        password=h
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return UserOut (
    username=user.username,
    email=user.email,
    age=user.age
)

Base.metadata.create_all(bind=engine)