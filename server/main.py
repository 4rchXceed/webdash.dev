from fastapi import FastAPI, Depends, UploadFile, File, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from typing import Annotated
from config import Config
import base64
import os

load_dotenv()  # take environment variables from .env.

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = Config(config_dir="config")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

admin_token = os.getenv(
    "ADMIN_TOKEN"
)  # Yeah, this is not very secure, but it's just a personal project.

# Public part


@app.get("/siteconfig/get/all")
def read_all():
    return {
        "whoami": config.whoami,
        "projects": config.projects,
        "hobbies": config.hobbies,
        "knowledge": config.knowledge,
        "timeline": config.timeline,
        "general_footer": config.general_footer,
    }


@app.get("/siteconfig/get/{config_name}")
def read_config(config_name: str):
    if config_name == "whoami":
        return config.whoami
    elif config_name == "projects":
        return config.projects
    elif config_name == "hobbies":
        return config.hobbies
    elif config_name == "knowledge":
        return config.knowledge
    elif config_name == "timeline":
        return config.timeline
    elif config_name == "general_footer":
        return config.general_footer
    else:
        return {"status": "error", "message": "Invalid config name"}


@app.get("/site/images/{image_name}", responses={200: {"content": {"image/*": {}}}})
def get_image(image_name: str):
    if image_name + ".safename" not in os.listdir("db/images"):
        return {"status": "error", "message": "Image not found"}
    with open(f"db/images/{image_name}.safename", "rb") as image_file:
        imagedata = image_file.read()
    with open(f"db/images/{image_name}.meta", "r") as meta_file:
        content_type = meta_file.read()

    return Response(content=imagedata, media_type=content_type)


# Authentication part


@app.post("/site/login")
def login(form_data: Annotated[dict, Depends(oauth2_scheme)]):
    if form_data == admin_token:
        return {"status": "success", "message": "Login successful"}
    return {"status": "error", "message": "Invalid credentials"}


@app.post("/siteconfig/admin/set/{config_name}")
def set_config(
    config_name: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    data: dict = Body(...),
):
    if token != admin_token:
        return {"status": "error", "message": "Invalid token"}
    config.set_config(config_name, data["data"])
    return {"status": "success", "message": f"{config_name} updated successfully"}


@app.post("/site/images/upload")
async def upload_image(
    token: Annotated[str, Depends(oauth2_scheme)],
    file: UploadFile = File(...),
):
    if token != admin_token:
        return {"status": "error", "message": "Invalid token"}
    imagedata = await file.read()

    if not file.filename or file.filename in os.listdir("db/images"):
        return {"status": "error", "message": "Invalid filename"}

    if not file.content_type or not file.content_type.startswith("image/"):
        return {"status": "error", "message": "File is not an image"}

    name = base64.urlsafe_b64encode(file.filename.encode()).decode()
    with open(
        f"db/images/{name}.safename",  # Save with base64 name to avoid issues (e.g. ../)
        "wb",
    ) as image_file:
        image_file.write(imagedata)

    with open(f"db/images/{name}.meta", "w") as meta_file:
        meta_file.write(
            file.content_type
        )  # Save original content type in meta file -> to be used when serving
    return {
        "status": "success",
        "image_name": name,
        "message": "Image uploaded successfully",
    }
