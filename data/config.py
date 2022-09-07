import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv('TOKEN'))

# Список адміністраторів бота
ADMINS = [
    724806849,
    # 5208586312
]

HOST = os.getenv('HOST')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{HOST}/{DATABASE}'
