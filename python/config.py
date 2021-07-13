# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
