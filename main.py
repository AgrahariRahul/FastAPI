from fastapi import FastAPI, Depends, HTTPException,Header
from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone

app = FastAPI()


SECRET_KEY = "MYSECRETKEY"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token
    
def verify_access_token(token:str = Header(None)):
    try:
        payload = jwt.decode(token=token,key=SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except:
        raise HTTPException(
             status_code=401,
             detail = "Invalid access token"
        )
           
                                

@app.post("/login")
def login(username:str, passwd:str):
    if(username != "Rahul" or passwd !="1234"):
        raise HTTPException(
            status_code=401,
            detail= "Invalid username or password"
        )
    token = create_access_token({"username":username})
    return {
         "access_token": token
    }
 
@app.get("/dashboard")    
def dashboard(user = Depends(verify_access_token)):
    return {
                "message" : "Secure data access",
                "data": "dashboard"
            }   
                