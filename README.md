# FaceToMesh

## Setup

### Prereqs

- docker
- npm (use nvm to install lts)
- python3 (and pip)

### Docker

see [https://github.com/AaronJackson/vrn-docker](https://github.com/AaronJackson/vrn-docker)

```bash
sudo docker pull asjackson/vrn:latest
```

### Python

install via pip

- fastapi
- uvicorn
- aiofiles

### FirstRun

Before the first run, the frontend has to be 'compiled'

```bash
cd frontend/face-frontend
npm install
npm run build
```

## Usage

```bash
uvicorn test_api:main --host 0.0.0.0 --port 8000 --reload
```

- open your browser at [http://localhost:8000](http://localhost:8000)
- use the file picker at the top to select a ***JPG*** file
- when selected, the file is automatically uploaded and processed.
- after conversion is completed, the webapp will be expanded with a new renderer
- you can find the model files (obj and ply) alongside the images (original and cropped) inside the data folder

## Known bugs

- only works with jpg images
- old renderers stop taking mouse inputs when a new one is created
