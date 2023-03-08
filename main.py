import uvicorn
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from settings import Settings
from io import BytesIO
from openpyxl import load_workbook
from zipfile import BadZipFile
from utils import optimum, fifo, not_recently_used, InvalidTable

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
    sheet = load_workbook(BytesIO(await file.read()), data_only=True).active
    algorithms = [optimum, not_recently_used, fifo]
    
    for algorithm in algorithms:
      try: 
        title, references, fails = algorithm(sheet)
        break
      except AssertionError:
        print('passing algorithm...')

    return JSONResponse({'data': {
      'algorithm': title,
      'performance': f'{((1 - (fails / references)) * 100):.2f}%',
      'frequency': f'{(fails / references):.2f}',
      'fails': fails,
      'references': references
    }}, 200)
  except InvalidTable as e:
    return JSONResponse({'error': str(e)})
  except BadZipFile:
    return JSONResponse({'error': 'Este no es un archivo excel válido.'}, 400)
  except AssertionError as e:
    return JSONResponse({'error': str(e)}, 400)
  except Exception as e:
    return JSONResponse({'error': 'Algoritmo no encontrado.'}, 400)

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
