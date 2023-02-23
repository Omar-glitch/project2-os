from pydantic import BaseSettings
from dotenv import load_dotenv
from os import environ

load_dotenv('.env')

class Settings(BaseSettings):
  port : int = environ['PORT']
  host : str = environ['HOST']
  reload : bool = environ['DEBUG_MODE']