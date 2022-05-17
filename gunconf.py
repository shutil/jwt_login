from dotenv import load_dotenv
import os

load_dotenv(os.getcwd()+".gunicron.env")

KEYFILE=os.getenv('KEYFILE')
CERTFILE=os.getenv('CERTFILE')
