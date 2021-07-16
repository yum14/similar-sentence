# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
import os

load_dotenv()

FIREBASE_CONFIG = os.getenv('FIREBASE_CONFIG')
NEEDS_AUCHENTICATION = os.getenv('NEEDS_AUCHENTICATION')
