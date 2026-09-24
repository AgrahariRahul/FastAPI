from fastapi import FastAPI, Depends, HTTPException,Header # pyright: ignore[reportMissingImports]
from jose import JWTError, jwt # pyright: ignore[reportMissingModuleSource]
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # pyright: ignore[reportMissingImports]
from datetime import datetime, timedelta,timezone
from passlib.context import CryptContext # pyright: ignore[reportMissingImports]

app = FastAPI()


SECRET_KEY = "MYSECRETKEY"
ALGORITHM = "HS256"

pass_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Dummy user DB
fake_user_db = {
    "admin":{
        "username":"admin",
        "hashed_password":pass_context.hash("1234")
    }
}

def hash_password(password:str):
    return pass_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pass_context.verify(plain_password,hashed_password)



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token
    
def verify_access_token(token:str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token=token,key=SECRET_KEY,algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail = "Invalid access token"
            )
        return username
    except JWTError:
        raise HTTPException(
             status_code=401,
             detail = "Invalid access token"
        )
           
                                

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail = "Invalid username or password"
        )
    token = create_access_token({"sub": form_data.username})
    return {
         "access_token": token,
          "token_type":"bearer"
    }

@app.get("/dashboard")    
def dashboard(user = Depends(verify_access_token)):
    return {
                "message" : "Secure data access",
                "data": "dashboard"
            }   
                