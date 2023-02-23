import uvicorn
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from settings import Settings
from io import BytesIO
import openpyxl
from zipfile import BadZipFile

settings = Settings()
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
async def home(request : Request):
  return templates.TemplateResponse('index.html', {'request': request})

@app.post('/')
async def get_type(file : UploadFile):
  try:
    openpyxl.load_workbook(BytesIO(await file.read()), data_only=True)
    return JSONResponse({'data': 'Este es un archivo excel.'}, 200)
  except BadZipFile:
    return JSONResponse({'error': 'Este no es un archivo excel válido.'}, 400)
  except Exception as e:
    print(type(e).__name__)
    return JSONResponse({'error': 'Este archivo no es válido.'}, 400)

@app.on_event('startup')
async def startup():
  print('# Starting server')

@app.on_event('shutdown')
def shutdown():
  print('# Shutting down server')

if __name__ == '__main__':
  uvicorn.run(
    "main:app",
    host=settings.host,
    reload=settings.reload,
    port=settings.port
  )
