from fastapi import FastAPI, UploadFile, File,HTTPException,Request
from fastapi.staticfiles import StaticFiles
import os
import shutil


app  = FastAPI()

UPLOAD_DIR = "uploads"

def create_upload_dir():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
create_upload_dir()        
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

@app.post("/upload")
def file_upload(request: Request,file: UploadFile = File("...")):
    file_name = file.filename
    if not file_name:
        raise HTTPException(
            status_code= 400,
            detail = "File Not Selected.."
        )
    file_path = os.path.join(UPLOAD_DIR,file_name)    
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
        
        return{
            "message":"File Upload successfully",
            "file_name":file_name,
            "file_url": request.url_for("files",path=file_name)
        }


@app.get("/getfiles")
def get_file(request: Request,file_name:str):
    file_path = os.path.join(UPLOAD_DIR,file_name)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=402,
            detail= "File not exists."
        )
    return {
        "file_url": request.url_for("files",path=file_name)
    }    
    
                    

