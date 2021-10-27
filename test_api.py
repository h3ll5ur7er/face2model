from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.responses import FileResponse
import uvicorn

from face2model import run
from obj2ply import convert

main = Starlette()
frontend = Starlette()
backend = FastAPI()

# SPA routing
@frontend.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return FileResponse('./frontend/face-frontend/dist/face-frontend/index.html')
    return response
@frontend.exception_handler(404)
def not_found(request, exc):
    return FileResponse('./frontend/face-frontend/dist/face-frontend/index.html')

# Static files
frontend.mount('/', StaticFiles(directory='./frontend/face-frontend/dist/face-frontend/'))
main.mount("/data", StaticFiles(directory="./data"), name="data")

# API
@backend.post("/convert")
async def create_upload_file(image: UploadFile  = File(..., media_type="image/*")):
    content = await image.read()
    print(image.filename, len(content))
    input_image = f"data/{image.filename}"
    with open(input_image, "wb") as f:
        f.write(content)
    run(image.filename)
    convert(f"{input_image}.obj", f"{input_image}.ply")
    return True


main.mount('/api', app=backend)
main.mount('/', app=frontend)

if __name__ == "__main__":
    uvicorn.run(main, host="0.0.0.0", port=8000)
